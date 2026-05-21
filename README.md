# StudyHub file upload + download

This project serves `studyhub.html` and adds real file upload/download endpoints.

## Why friends don't see your files

StudyHub stores PDFs on the **server** (`data/uploads/`) and lists them from `data/index.json`. If you only send:

- the `studyhub.html` file, or
- `http://127.0.0.1:8000` (your laptop),

your friend is not using your server, so downloads and community attachments will be missing.

**Fix:** host the app on a public URL (below) and/or put files on **Google Drive** with “Anyone with the link”.

## Run locally

```bash
cd /Users/anjil/Documents/work.py
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:8000` and share **that** link only while your computer is on (not ideal for friends).

## Share with friends (recommended)

### Option A — Deploy the full app (files already in git)

1. Push this repo to GitHub (`menote`).
2. On [Render](https://render.com), create a **Web Service** from the repo (this repo includes `render.yaml`).
3. After deploy, share the Render URL (e.g. `https://studyhub-xxxx.onrender.com`).

Friends use the same server and get syllabi/notes that are committed under `data/uploads/`.

### Option B — Google Drive links (best for new uploads)

1. Upload the PDF to Google Drive.
2. Right-click → **Share** → **General access: Anyone with the link** (Viewer).
3. Copy the share link.
4. In StudyHub → **Community** tab, paste the link in **Or Google Drive link** (do not rely on a local file only).

For bulk syllabus seeding, add entries in `seed/manifest.json` with `"external_url": "https://drive.google.com/..."` and no `"path"` (see `seed/manifest.example.json`), then run `python seed_uploads.py`.

Drive links are stored in `data/index.json` / community posts; downloads open Google’s servers, so friends do not need your laptop.

## Seed initial files (developer upload first)

1) Put your files under `seed/` (any subfolders you want), and create `seed/manifest.json` by copying:

```bash
cp seed/manifest.example.json seed/manifest.json
```

2) Edit `seed/manifest.json` and list your files + metadata (faculty/semester/subject/etc). Use `external_url` for Drive-hosted files.

3) Run:

```bash
python seed_uploads.py
```

This copies local files into `data/uploads/...` and updates `data/index.json`.

## Where files are stored

- Uploaded files: `data/uploads/<category>/...`
- Metadata index: `data/index.json`
- Community uploads: `data/community/uploads/...`

## API: upload with Google Drive

`POST /api/upload/<category>` with form field `external_url` (and optional `file`). Category is `notes`, `past-papers`, or `syllabus`.

Community posts: `POST /api/community/posts` with `external_url` instead of `file`.
