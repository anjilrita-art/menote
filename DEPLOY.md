# Deploy StudyHub (one-time setup)

After you push this repo to GitHub, deploy on Render so friends can open one link and download files.

## Steps

1. Push the latest code:
   ```bash
   git push origin main
   ```

2. Open [https://dashboard.render.com/select-repo?type=blueprint](https://dashboard.render.com/select-repo?type=blueprint)

3. Connect GitHub account → choose repository **anjilrita-art/menote** (or your fork).

4. Render reads `render.yaml` and creates a **studyhub** web service. Click **Apply**.

5. Wait for the build (~2–5 minutes). Copy the URL, e.g. `https://studyhub-xxxx.onrender.com`.

6. Share that URL with friends (not `127.0.0.1` and not the raw HTML file).

## Free tier note

The service sleeps after ~15 minutes idle; the first visit may take ~30 seconds to wake up.

## New uploads with Google Drive

For community posts, use **Or Google Drive link** with sharing set to **Anyone with the link** so files stay available even if the server restarts.
