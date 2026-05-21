from __future__ import annotations

import json
import mimetypes
import os
import re
from urllib.parse import urlparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from flask import Flask, jsonify, redirect, request, send_file, send_from_directory

from drive_links import normalize_external_url


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
INDEX_PATH = DATA_DIR / "index.json"

COMMUNITY_DIR = DATA_DIR / "community"
COMMUNITY_UPLOADS_DIR = COMMUNITY_DIR / "uploads"
COMMUNITY_INDEX_PATH = COMMUNITY_DIR / "posts.json"

GITHUB_RAW_REPO = os.environ.get("GITHUB_RAW_REPO", "anjilrita-art/menote")
GITHUB_RAW_BRANCH = os.environ.get("GITHUB_RAW_BRANCH", "main")

Category = Literal["notes", "past-papers", "syllabus"]
ALLOWED_CATEGORIES: set[str] = {"notes", "past-papers", "syllabus"}


@dataclass(frozen=True)
class FileEntry:
    id: str
    category: str
    original_name: str
    stored_name: str
    content_type: str
    size_bytes: int
    uploaded_at: str  # ISO8601 UTC
    meta: dict[str, Any]
    external_url: str | None = None


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


_FILENAME_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_filename(name: str) -> str:
    name = os.path.basename(name or "file")
    name = name.strip().replace(" ", "_")
    name = _FILENAME_SAFE_RE.sub("_", name)
    if not name or name in {".", ".."}:
        return "file"
    return name[:180]


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    for cat in ALLOWED_CATEGORIES:
        (UPLOADS_DIR / cat).mkdir(parents=True, exist_ok=True)
    COMMUNITY_DIR.mkdir(parents=True, exist_ok=True)
    COMMUNITY_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def _load_index() -> dict[str, Any]:
    _ensure_dirs()
    if not INDEX_PATH.exists():
        return {"files": []}
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except Exception:
        # If index becomes corrupted, don't crash the app.
        return {"files": []}


def _save_index(index: dict[str, Any]) -> None:
    _ensure_dirs()
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _get_entry(index: dict[str, Any], file_id: str) -> FileEntry | None:
    for item in index.get("files", []):
        if item.get("id") == file_id:
            try:
                return FileEntry(**item)
            except Exception:
                return None
    return None


def _github_raw_url(path: str) -> str:
    path = path.lstrip("/")
    return f"https://raw.githubusercontent.com/{GITHUB_RAW_REPO}/{GITHUB_RAW_BRANCH}/{path}"


def _category_or_404(raw: str | None) -> str:
    if not raw or raw not in ALLOWED_CATEGORIES:
        raise ValueError("Invalid category")
    return raw


app = Flask(__name__, static_folder=None)

@app.after_request
def _add_cors_headers(resp):
    # Let the frontend be served from another origin (e.g. VSCode Live Server)
    # while the API runs on http://127.0.0.1:8000.
    resp.headers.setdefault("Access-Control-Allow-Origin", "*")
    resp.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    resp.headers.setdefault("Access-Control-Allow-Headers", "Content-Type")
    return resp


@app.route("/api/<path:_any>", methods=["OPTIONS"])
def _cors_preflight(_any: str):
    return ("", 204)


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "studyhub.html")


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.get("/api/config")
def public_config():
    return jsonify(
        {
            "public_site_url": f"https://{GITHUB_RAW_REPO.split('/')[0]}.github.io/{GITHUB_RAW_REPO.split('/')[1]}/",
            "github_repo": GITHUB_RAW_REPO,
            "github_branch": GITHUB_RAW_BRANCH,
            "file_count": len(_load_index().get("files", [])),
        }
    )


@app.get("/api/files/<category>")
def list_files(category: str):
    try:
        category = _category_or_404(category)
    except ValueError:
        return jsonify({"error": "Invalid category"}), 400

    index = _load_index()
    files = [f for f in index.get("files", []) if f.get("category") == category]
    files.sort(key=lambda x: x.get("uploaded_at", ""), reverse=True)
    return jsonify({"files": files})


def _parse_external_url(raw: str | None) -> str | None:
    value = (raw or "").strip()
    if not value:
        return None
    try:
        return normalize_external_url(value)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc


@app.post("/api/upload/<category>")
def upload(category: str):
    try:
        category = _category_or_404(category)
    except ValueError:
        return jsonify({"error": "Invalid category"}), 400

    try:
        external_url = _parse_external_url(request.form.get("external_url"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    f = request.files.get("file")
    has_file = bool(f and f.filename)

    if not has_file and not external_url:
        return jsonify({"error": "Provide a file upload or a Google Drive / external link"}), 400

    meta: dict[str, Any] = {}
    for key in request.form:
        if key != "external_url":
            meta[key] = request.form.get(key)

    file_id = uuid4().hex
    stored_name = ""
    content_type = "application/octet-stream"
    size_bytes = 0
    original_name = (request.form.get("title") or request.form.get("original_name") or "external-link").strip()

    if has_file:
        original_name = f.filename or original_name
        safe_original = _safe_filename(original_name)
        stored_name = f"{file_id}__{safe_original}"
        content_type = f.mimetype or ""
        if not content_type or content_type == "application/octet-stream":
            guessed, _ = mimetypes.guess_type(safe_original)
            content_type = guessed or "application/octet-stream"
        _ensure_dirs()
        dst = UPLOADS_DIR / category / stored_name
        f.save(dst)
        size_bytes = dst.stat().st_size
    elif external_url:
        guessed_name = (request.form.get("original_name") or "").strip()
        if guessed_name:
            original_name = guessed_name
        elif not original_name or original_name == "external-link":
            original_name = "Google Drive file"

    entry = FileEntry(
        id=file_id,
        category=category,
        original_name=original_name,
        stored_name=stored_name,
        content_type=content_type,
        size_bytes=size_bytes,
        uploaded_at=_now_iso_utc(),
        meta=meta,
        external_url=external_url,
    )

    index = _load_index()
    index.setdefault("files", []).append(asdict(entry))
    _save_index(index)

    return jsonify({"ok": True, "file": asdict(entry)})


@app.get("/download/<file_id>")
def download(file_id: str):
    index = _load_index()
    entry = _get_entry(index, file_id)
    if not entry:
        return jsonify({"error": "File not found"}), 404

    if entry.external_url:
        # Safety: only allow http(s) redirects.
        parsed = urlparse(entry.external_url)
        if parsed.scheme in {"http", "https"}:
            return redirect(entry.external_url, code=302)
        return jsonify({"error": "Invalid external link"}), 400

    path = UPLOADS_DIR / entry.category / entry.stored_name
    if not path.exists():
        if entry.stored_name and GITHUB_RAW_REPO:
            return redirect(
                _github_raw_url(f"data/uploads/{entry.category}/{entry.stored_name}"),
                code=302,
            )
        return jsonify({"error": "File missing on server"}), 404

    return send_file(
        path,
        as_attachment=True,
        download_name=_safe_filename(entry.original_name),
        mimetype=entry.content_type or None,
        conditional=True,
        max_age=0,
    )


def _load_posts() -> dict[str, Any]:
    _ensure_dirs()
    if not COMMUNITY_INDEX_PATH.exists():
        return {"posts": []}
    try:
        return json.loads(COMMUNITY_INDEX_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"posts": []}


def _save_posts(posts: dict[str, Any]) -> None:
    _ensure_dirs()
    COMMUNITY_INDEX_PATH.write_text(json.dumps(posts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@app.get("/api/community/posts")
def community_list_posts():
    data = _load_posts()
    posts = data.get("posts", [])
    posts.sort(key=lambda p: (p.get("score", 0), p.get("created_at", "")), reverse=True)
    return jsonify({"posts": posts})


@app.post("/api/community/posts")
def community_create_post():
    title = (request.form.get("title") or "").strip()
    body = (request.form.get("body") or "").strip()
    faculty = (request.form.get("faculty") or "").strip()
    semester = (request.form.get("semester") or "").strip()
    subject = (request.form.get("subject") or "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400

    try:
        external_url = _parse_external_url(request.form.get("external_url"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    attachment = request.files.get("file")
    stored_name = None
    original_name = None
    content_type = None
    size_bytes = None

    if attachment and attachment.filename:
        original_name = attachment.filename
        safe_original = _safe_filename(original_name)
        post_id = uuid4().hex
        stored_name = f"{post_id}__{safe_original}"

        content_type = attachment.mimetype or ""
        if not content_type or content_type == "application/octet-stream":
            guessed, _ = mimetypes.guess_type(safe_original)
            content_type = guessed or "application/octet-stream"

        _ensure_dirs()
        dst = COMMUNITY_UPLOADS_DIR / stored_name
        attachment.save(dst)
        size_bytes = dst.stat().st_size
    elif external_url:
        post_id = uuid4().hex
        original_name = (request.form.get("file_name") or title or "Google Drive file").strip()
    else:
        post_id = uuid4().hex

    post = {
        "id": post_id,
        "title": title,
        "body": body,
        "created_at": _now_iso_utc(),
        "score": 0,
        "meta": {
            "faculty": faculty,
            "semester": semester,
            "subject": subject,
        },
        "attachment": (
            None
            if not stored_name and not external_url
            else {
                "stored_name": stored_name,
                "original_name": original_name,
                "content_type": content_type,
                "size_bytes": size_bytes,
                "external_url": external_url,
            }
        ),
    }

    data = _load_posts()
    data.setdefault("posts", []).append(post)
    _save_posts(data)
    return jsonify({"ok": True, "post": post})


@app.post("/api/community/vote/<post_id>")
def community_vote(post_id: str):
    payload = request.get_json(silent=True) or {}
    direction = payload.get("direction")
    if direction not in ("up", "down"):
        return jsonify({"error": "direction must be 'up' or 'down'"}), 400

    data = _load_posts()
    posts = data.get("posts", [])
    for p in posts:
        if p.get("id") == post_id:
            p["score"] = int(p.get("score", 0)) + (1 if direction == "up" else -1)
            _save_posts(data)
            return jsonify({"ok": True, "post": p})

    return jsonify({"error": "Post not found"}), 404


@app.get("/community/download/<post_id>")
def community_download(post_id: str):
    data = _load_posts()
    posts = data.get("posts", [])
    post = next((p for p in posts if p.get("id") == post_id), None)
    if not post or not post.get("attachment"):
        return jsonify({"error": "File not found"}), 404

    att = post["attachment"]
    ext = att.get("external_url")
    if ext:
        parsed = urlparse(ext)
        if parsed.scheme in {"http", "https"}:
            return redirect(ext, code=302)
        return jsonify({"error": "Invalid external link"}), 400

    stored_name = att["stored_name"]
    if not stored_name:
        return jsonify({"error": "File not found"}), 404
    original_name = post["attachment"]["original_name"] or "file"
    content_type = post["attachment"].get("content_type") or None

    path = COMMUNITY_UPLOADS_DIR / stored_name
    if not path.exists():
        if stored_name and GITHUB_RAW_REPO:
            return redirect(
                _github_raw_url(f"data/community/uploads/{stored_name}"),
                code=302,
            )
        return jsonify({"error": "File missing on server"}), 404

    return send_file(
        path,
        as_attachment=True,
        download_name=_safe_filename(original_name),
        mimetype=content_type,
        conditional=True,
        max_age=0,
    )


if __name__ == "__main__":
    _ensure_dirs()
    port = int(os.environ.get("PORT", "8000"))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(host="0.0.0.0", port=port, debug=debug)

