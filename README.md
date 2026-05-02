# StudyHub file upload + download

This project serves `studyhub.html` and adds real file upload/download endpoints.

## Run locally

```bash
cd /Users/anjil/Documents/work.py
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:8000`.

## Seed initial files (developer upload first)

1) Put your files under `seed/` (any subfolders you want), and create `seed/manifest.json` by copying:

```bash
cp seed/manifest.example.json seed/manifest.json
```

2) Edit `seed/manifest.json` and list your files + metadata (faculty/semester/subject/etc).

3) Run:

```bash
python seed_uploads.py
```

This copies files into `data/uploads/...` and updates `data/index.json`.

## Where files are stored

- Uploaded files: `data/uploads/<category>/...`
- Metadata index: `data/index.json`

