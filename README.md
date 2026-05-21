# StudyHub — public IOE study materials

Anyone can browse and download notes, past papers, and syllabi.

## Public link (share this)

**https://anjilrita-art.github.io/menote/**

After you push to `main`, GitHub Actions publishes the site automatically (see `.github/workflows/pages.yml`). First deploy may take 2–5 minutes.

All PDFs are served from this GitHub repository, so downloads work for everyone without logging in.

## Run locally (optional)

```bash
cd /Users/anjil/Documents/work.py
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:8000`.

## Full server (uploads + community posting)

Deploy on [Render](https://render.com) using `render.yaml` — see [DEPLOY.md](DEPLOY.md). Use this if you need upload APIs; for **download-only** access, the GitHub Pages link above is enough.

## Google Drive (optional uploads)

In the Community tab, paste a Drive link with **Anyone with the link** access so files stay public.

## Seed files (developer)

```bash
cp seed/manifest.example.json seed/manifest.json
# edit manifest — use external_url for Drive-hosted PDFs
python seed_uploads.py
```

## Data layout

- `data/uploads/<category>/` — PDF files
- `data/index.json` — catalog (166 entries)
- `data/community/` — community posts and attachments
