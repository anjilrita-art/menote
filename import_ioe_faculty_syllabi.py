from __future__ import annotations

import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BASE_DIR = Path(__file__).resolve().parent
SEED_DIR = BASE_DIR / "seed"
MANIFEST_PATH = SEED_DIR / "manifest.json"

YEAR_ROMAN_TO_INT = {"I": 1, "II": 2, "III": 3, "IV": 4}
PART_ROMAN_TO_INT = {"I": 1, "II": 2}


@dataclass(frozen=True)
class CourseLink:
    semester: str
    course_code: str
    title: str
    url: str
    kind: str  # "syllabus" | "micro"


HEADING_RE = re.compile(r"^Year\s+(I|II|III|IV):\s+Part\s+(I|II)\s*$")

# | 1 | ENCE 101 | [Engineering Mechanics](https://...) | ...
ROW_LINK_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*([A-Z]{2,}\s*\d+(?:-\d+)?)\s*\|\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*\|"
)

# | 1 | ENCE 401 | Operations Research | 2 |
ROW_PLAIN_RE = re.compile(r"^\|\s*\d+\s*\|\s*([A-Z]{2,}\s*\d+(?:-\d+)?)\s*\|\s*([^|]+?)\s*\|\s*\d+")

MICRO_RE = re.compile(r"\[Micro-Syllabus\]\((https?://[^)]+)\)")


def semester_from_heading(year_roman: str, part_roman: str) -> str:
    year = YEAR_ROMAN_TO_INT[year_roman]
    part = PART_ROMAN_TO_INT[part_roman]
    return str((year - 1) * 2 + part)


def safe_filename(name: str) -> str:
    out = []
    for ch in name.strip():
        if ch.isalnum() or ch in "._-":
            out.append(ch)
        elif ch.isspace():
            out.append("_")
        else:
            out.append("_")
    cleaned = "".join(out)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return (cleaned or "file")[:180]


def download(url: str, dst: Path, retries: int = 2) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size > 0:
        return

    headers = {"User-Agent": "StudyHubSeeder/1.0 (+local)"}
    req = urllib.request.Request(url, headers=headers)

    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    allow_insecure_for_host = host.endswith("portal.tu.edu.np")

    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    data = r.read()
            except ssl.SSLCertVerificationError:
                if not allow_insecure_for_host:
                    raise
                ctx = ssl._create_unverified_context()  # noqa: SLF001
                with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                    data = r.read()
            dst.write_bytes(data)
            return
        except ssl.SSLCertVerificationError as e:
            last_err = e
            time.sleep(1.2 * attempt)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            # SSL error may be wrapped in URLError
            if (
                allow_insecure_for_host
                and isinstance(e, urllib.error.URLError)
                and isinstance(getattr(e, "reason", None), ssl.SSLCertVerificationError)
            ):
                try:
                    ctx = ssl._create_unverified_context()  # noqa: SLF001
                    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                        data = r.read()
                    dst.write_bytes(data)
                    return
                except Exception as e2:  # noqa: BLE001
                    last_err = e2
                    time.sleep(1.2 * attempt)
                    continue
            last_err = e
            time.sleep(1.2 * attempt)

    raise RuntimeError(f"Failed to download after {retries} attempts: {url}\n{last_err}")


def iter_courses_from_markdown(md_lines: Iterable[str]) -> tuple[list[CourseLink], dict[str, list[str]]]:
    semester: str | None = None
    links: list[CourseLink] = []
    subjects_by_sem: dict[str, list[str]] = {}

    def add_subject(sem: str, title: str) -> None:
        title = title.strip()
        if not title:
            return
        subjects_by_sem.setdefault(sem, [])
        if title not in subjects_by_sem[sem]:
            subjects_by_sem[sem].append(title)

    for line in md_lines:
        line = line.strip("\n")

        hm = HEADING_RE.match(line.strip())
        if hm:
            semester = semester_from_heading(hm.group(1), hm.group(2))
            continue

        if semester is None:
            continue

        m = ROW_LINK_RE.match(line)
        if m:
            course_code = m.group(1).replace(" ", "")
            title = m.group(2).strip()
            url = m.group(3).strip()
            add_subject(semester, title)
            links.append(CourseLink(semester, course_code, title, url, "syllabus"))
            micro = MICRO_RE.search(line)
            if micro:
                links.append(CourseLink(semester, course_code, title, micro.group(1), "micro"))
            continue

        mp = ROW_PLAIN_RE.match(line)
        if mp:
            title = mp.group(2).strip()
            add_subject(semester, title)

    # Sort subjects
    for sem in subjects_by_sem:
        subjects_by_sem[sem].sort(key=lambda s: s.lower())

    # De-dupe links
    uniq: dict[tuple[str, str, str, str], CourseLink] = {}
    failed: list[str] = []
    for c in links:
        uniq[(c.semester, c.course_code, c.kind, c.url)] = c
    return list(uniq.values()), subjects_by_sem


def load_or_init_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {"files": []}


def ensure_manifest_has_entries(manifest: dict, entries: list[dict]) -> int:
    files = manifest.setdefault("files", [])
    if not isinstance(files, list):
        raise ValueError("seed/manifest.json must contain {\"files\": [...]}")

    def key(e: dict) -> tuple:
        meta = e.get("meta") or {}
        return (
            e.get("category"),
            e.get("path"),
            e.get("original_name"),
            meta.get("faculty"),
            meta.get("semester"),
            meta.get("subject"),
            meta.get("code"),
            meta.get("type"),
        )

    existing = {key(e) for e in files if isinstance(e, dict)}
    added = 0
    for e in entries:
        k = key(e)
        if k in existing:
            continue
        files.append(e)
        existing.add(k)
        added += 1
    return added


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Download IOE syllabi + write subjects map")
    parser.add_argument("--faculty", required=True, help="Faculty code like BEX, BMX, BCE, BEL")
    parser.add_argument(
        "--curriculum",
        required=True,
        help="Path to curriculum markdown (from WebFetch or saved copy)",
    )
    args = parser.parse_args()

    faculty = args.faculty.strip().upper()
    curriculum_md = Path(args.curriculum).expanduser().resolve()
    if not curriculum_md.exists():
        raise SystemExit(f"Missing curriculum markdown: {curriculum_md}")

    lines = curriculum_md.read_text(encoding="utf-8", errors="replace").splitlines()
    links, subjects_by_sem = iter_courses_from_markdown(lines)
    links.sort(key=lambda c: (int(c.semester), c.course_code, c.kind))

    seed_out_dir = SEED_DIR / "syllabus" / f"ioe_{faculty.lower()}"
    seed_out_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_or_init_manifest()
    new_entries: list[dict] = []
    failed: list[str] = []

    for c in links:
        parsed = urllib.parse.urlparse(c.url)
        filename = Path(urllib.parse.unquote(parsed.path)).name or f"{c.course_code}.pdf"
        kind_suffix = "_micro" if c.kind == "micro" else ""
        seed_name = safe_filename(f"{faculty}_Sem{c.semester}_{c.course_code}_{c.title}{kind_suffix}.pdf")
        rel_path = f"syllabus/ioe_{faculty.lower()}/{seed_name}"
        dst = SEED_DIR / rel_path

        print(f"Downloading sem{c.semester} {c.course_code} ({c.kind})...", flush=True)
        try:
            download(c.url, dst)
        except Exception as e:  # noqa: BLE001
            failed.append(f"{c.course_code} {c.kind}: {c.url} ({e})")
            continue

        meta = {
            "faculty": faculty,
            "semester": c.semester,
            "subject": c.title,
            "code": c.course_code,
            "instructor": "IOE",
        }
        if c.kind == "micro":
            meta["type"] = "Micro-Syllabus"

        new_entries.append(
            {
                "category": "syllabus",
                "path": rel_path,
                "original_name": filename,
                "meta": meta,
            }
        )

    added = ensure_manifest_has_entries(manifest, new_entries)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subjects_json_path = SEED_DIR / "curricula" / f"subjects_{faculty.lower()}.json"
    subjects_json_path.write_text(json.dumps({faculty: subjects_by_sem}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Found {sum(len(v) for v in subjects_by_sem.values())} subjects across {len(subjects_by_sem)} semesters")
    downloaded = sum(1 for e in new_entries if (SEED_DIR / e["path"]).exists())
    print(f"Downloaded {downloaded} PDFs into {seed_out_dir}")
    print(f"Added {added} manifest entries in {MANIFEST_PATH}")
    print(f"Wrote subjects map to {subjects_json_path}")
    if failed:
        print(f"Failed downloads: {len(failed)}")
        for line in failed[:10]:
            print(f"- {line}")
        if len(failed) > 10:
            print(f"... and {len(failed) - 10} more")
    print("Next: run `python seed_uploads.py` to import into the app.")


if __name__ == "__main__":
    main()

