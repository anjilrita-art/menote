from __future__ import annotations

import json
import mimetypes
import os
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
INDEX_PATH = DATA_DIR / "index.json"

ALLOWED_CATEGORIES: set[str] = {"notes", "past-papers", "syllabus"}


@dataclass(frozen=True)
class FileEntry:
    id: str
    category: str
    original_name: str
    stored_name: str
    content_type: str
    size_bytes: int
    uploaded_at: str
    meta: dict[str, Any]
    external_url: str | None = None


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    for cat in ALLOWED_CATEGORIES:
        (UPLOADS_DIR / cat).mkdir(parents=True, exist_ok=True)


def _load_index() -> dict[str, Any]:
    _ensure_dirs()
    if not INDEX_PATH.exists():
        return {"files": []}
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def _save_index(index: dict[str, Any]) -> None:
    _ensure_dirs()
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _safe_filename(name: str) -> str:
    name = os.path.basename(name or "file").strip().replace(" ", "_")
    out = []
    for ch in name:
        if ch.isalnum() or ch in "._-":
            out.append(ch)
        else:
            out.append("_")
    cleaned = "".join(out)
    if not cleaned or cleaned in {".", ".."}:
        cleaned = "file"
    return cleaned[:180]


def _guess_type(path: Path) -> str:
    guessed, _ = mimetypes.guess_type(path.name)
    return guessed or "application/octet-stream"


def _file_already_seeded(index: dict[str, Any], category: str, original_name: str, meta: dict[str, Any]) -> bool:
    # Simple idempotency: if same category + original_name + key meta fields exist, skip.
    key_fields = ("faculty", "semester", "subject", "topic", "year", "type", "code", "instructor")
    for f in index.get("files", []):
        if f.get("category") != category:
            continue
        if f.get("original_name") != original_name:
            continue
        m = f.get("meta") or {}
        if all((m.get(k) or "") == (meta.get(k) or "") for k in key_fields):
            return True
    return False


def seed_from_manifest(manifest_path: Path) -> int:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ValueError("manifest.json must contain a top-level 'files' array")

    index = _load_index()
    created = 0

    for item in files:
        if not isinstance(item, dict):
            raise ValueError("Each manifest entry must be an object")

        category = item.get("category")
        if category not in ALLOWED_CATEGORIES:
            raise ValueError(f"Invalid category: {category!r}. Use one of: {sorted(ALLOWED_CATEGORIES)}")

        external_url = item.get("external_url")
        if external_url is not None and not isinstance(external_url, str):
            raise ValueError("'external_url' must be a string when provided")

        rel_path = item.get("path")
        if external_url:
            # Link-only entry: no local file required.
            rel_path = None
        else:
            if not isinstance(rel_path, str) or not rel_path.strip():
                raise ValueError("Each entry must have a non-empty 'path' (relative to seed folder) unless using external_url")

        meta = item.get("meta") or {}
        if not isinstance(meta, dict):
            raise ValueError("'meta' must be an object")

        src = None
        if rel_path:
            src = manifest_path.parent / rel_path
            if not src.exists() or not src.is_file():
                raise FileNotFoundError(f"Missing file: {src}")

        original_name = item.get("original_name") or (src.name if src else "external-link")
        original_name = str(original_name)

        if _file_already_seeded(index, category, original_name, meta):
            continue

        file_id = uuid4().hex
        stored_name = ""
        content_type = "application/octet-stream"
        size_bytes = 0

        if src:
            stored_name = f"{file_id}__{_safe_filename(original_name)}"
            dst = UPLOADS_DIR / category / stored_name
            _ensure_dirs()
            shutil.copy2(src, dst)
            content_type = _guess_type(dst)
            size_bytes = dst.stat().st_size

        entry = FileEntry(
            id=file_id,
            category=category,
            original_name=original_name,
            stored_name=stored_name,
            content_type=content_type,
            size_bytes=size_bytes,
            uploaded_at=_now_iso_utc(),
            meta={k: ("" if v is None else str(v)) for k, v in meta.items()},
            external_url=external_url,
        )

        index.setdefault("files", []).append(asdict(entry))
        created += 1

    _save_index(index)
    return created


def main() -> None:
    manifest_path = BASE_DIR / "seed" / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing {manifest_path}. Create it from seed/manifest.example.json")
    created = seed_from_manifest(manifest_path)
    print(f"Seed complete. Added {created} files.")


if __name__ == "__main__":
    main()

