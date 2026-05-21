"""Normalize Google Drive share links to direct-download URLs."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

_DRIVE_HOSTS = {
    "drive.google.com",
    "docs.google.com",
    "drive.usercontent.google.com",
}

_FILE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{10,}$")


def is_google_drive_url(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return False
    return host in _DRIVE_HOSTS or host.endswith(".googleusercontent.com")


def extract_file_id(url: str) -> str | None:
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    if host not in _DRIVE_HOSTS and not host.endswith(".googleusercontent.com"):
        return None

    # /file/d/<id>/...
    parts = [p for p in parsed.path.split("/") if p]
    if "file" in parts or "document" in parts:
        for i, part in enumerate(parts):
            if part in {"file", "document", "d"} and i + 1 < len(parts):
                candidate = parts[i + 1]
                if candidate not in {"view", "edit", "preview", "d"} and _FILE_ID_RE.match(candidate):
                    return candidate

    # ?id=<id>
    qs = parse_qs(parsed.query)
    for key in ("id", "export"):
        if key == "id" and qs.get("id"):
            candidate = qs["id"][0]
            if _FILE_ID_RE.match(candidate):
                return candidate

    # /uc?export=download&id=<id>
    if qs.get("id"):
        candidate = qs["id"][0]
        if _FILE_ID_RE.match(candidate):
            return candidate

    return None


def to_direct_download_url(url: str) -> str:
    """Turn a Drive share/view link into a link browsers can download from."""
    url = (url or "").strip()
    if not url:
        raise ValueError("Empty URL")
    file_id = extract_file_id(url)
    if not file_id:
        return url
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def normalize_external_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        raise ValueError("Empty URL")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must start with http:// or https://")
    if is_google_drive_url(url):
        return to_direct_download_url(url)
    return url
