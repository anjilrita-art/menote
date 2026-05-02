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
SEED_SYLLABUS_DIR = SEED_DIR / "syllabus" / "ioe_bel"
MANIFEST_PATH = SEED_DIR / "manifest.json"


@dataclass(frozen=True)
class CourseLink:
    semester: str
    course_code: str
    title: str
    url: str
    kind: str  # "syllabus" | "micro"


YEAR_ROMAN_TO_INT = {"I": 1, "II": 2, "III": 3, "IV": 4}
PART_ROMAN_TO_INT = {"I": 1, "II": 2}


def semester_from_heading(year_roman: str, part_roman: str) -> str:
    year = YEAR_ROMAN_TO_INT[year_roman]
    part = PART_ROMAN_TO_INT[part_roman]
    return str((year - 1) * 2 + part)


HEADING_RE = re.compile(r"^\*\*Year\s+(I|II|III|IV):\s+Part\s+(I|II)\*\*\s*$")

# Table row with linked title:
# | 1 | ENSH 101 | [Engineering Mathematics I](https://...) | ...
ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*([A-Z]{2,}\s*\d+(?:-\d+)?)\s*\|\s*\[([^\]]+)\]\((https?://[^)]+)\)\s*\|"
)

# Micro-syllabus appears later in the row as [Micro-Syllabus](https://...)
MICRO_RE = re.compile(r"\[Micro-Syllabus\]\((https?://[^)]+)\)")


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


def iter_courses_from_markdown(md_lines: Iterable[str]) -> list[CourseLink]:
    semester: str | None = None
    out: list[CourseLink] = []

    for line in md_lines:
        line = line.rstrip("\n")

        m = HEADING_RE.match(line)
        if m:
            semester = semester_from_heading(m.group(1), m.group(2))
            continue

        # Handle the truncated "**Year IV: Part**" heading in the saved page
        if line.strip() == "**Year IV: Part**":
            semester = "8"
            continue

        m = ROW_RE.match(line)
        if not m or semester is None:
            continue

        course_code = m.group(1).replace(" ", "")
        title = m.group(2).strip()
        url = m.group(3).strip()

        out.append(CourseLink(semester=semester, course_code=course_code, title=title, url=url, kind="syllabus"))

        micro = MICRO_RE.search(line)
        if micro:
            out.append(CourseLink(semester=semester, course_code=course_code, title=title, url=micro.group(1), kind="micro"))

    # De-dupe by (semester, course_code, kind, url)
    uniq: dict[tuple[str, str, str, str], CourseLink] = {}
    for c in out:
        uniq[(c.semester, c.course_code, c.kind, c.url)] = c
    return list(uniq.values())


def download(url: str, dst: Path, retries: int = 3) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size > 0:
        return

    headers = {"User-Agent": "StudyHubSeeder/1.0 (+local)"}
    req = urllib.request.Request(url, headers=headers)

    last_err: Exception | None = None
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    allow_insecure_for_host = host.endswith("portal.tu.edu.np")

    for attempt in range(1, retries + 1):
        try:
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
            except ssl.SSLCertVerificationError as e:
                if not allow_insecure_for_host:
                    raise
                # Local machines sometimes lack the CA chain for this host.
                # Fall back to an unverified context only for portal.tu.edu.np.
                ctx = ssl._create_unverified_context()  # noqa: SLF001
                with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                    data = r.read()
            dst.write_bytes(data)
            return
        except ssl.SSLCertVerificationError as e:
            last_err = e
            if not allow_insecure_for_host:
                time.sleep(1.2 * attempt)
                continue
            try:
                ctx = ssl._create_unverified_context()  # noqa: SLF001
                with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                    data = r.read()
                dst.write_bytes(data)
                return
            except Exception as e2:  # noqa: BLE001
                last_err = e2
                time.sleep(1.2 * attempt)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            # Sometimes SSL verification error is wrapped in URLError
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
    # Use the saved markdown copy that was attached in this chat.
    src_md = Path(
        "/Users/anjil/.cursor/projects/Users-anjil-Documents-work-py/uploads/electrical-engineering-curriculum-structure-2659-0.md"
    )
    if not src_md.exists():
        raise SystemExit(f"Missing curriculum markdown file: {src_md}")
    lines = src_md.read_text(encoding="utf-8", errors="replace").splitlines()

    courses = iter_courses_from_markdown(lines)
    courses.sort(key=lambda c: (int(c.semester), c.course_code, c.kind))

    manifest = load_or_init_manifest()

    new_entries: list[dict] = []
    for c in courses:
        parsed = urllib.parse.urlparse(c.url)
        filename = Path(urllib.parse.unquote(parsed.path)).name or f"{c.course_code}.pdf"

        # Save a local copy into seed folder
        kind_suffix = "_micro" if c.kind == "micro" else ""
        seed_name = safe_filename(f"BEL_Sem{c.semester}_{c.course_code}_{c.title}{kind_suffix}.pdf")
        rel_path = f"syllabus/ioe_bel/{seed_name}"
        dst = SEED_DIR / rel_path

        download(c.url, dst)

        meta = {
            "faculty": "BEL",
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
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Downloaded {len(courses)} PDFs into {SEED_SYLLABUS_DIR}")
    print(f"Added {added} manifest entries in {MANIFEST_PATH}")
    print("Next: run `python seed_uploads.py` to import into the app.")


if __name__ == "__main__":
    main()

