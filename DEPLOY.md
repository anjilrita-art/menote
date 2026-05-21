# Hosting options

## Option 1 — Public site for everyone (recommended)

**URL:** https://anjilrita-art.github.io/menote/

Push to `main` → GitHub Actions deploys automatically.

If the site 404s (one-time setup):

1. Open https://github.com/anjilrita-art/menote/settings/pages
2. **Build and deployment** → **Deploy from a branch**
3. Choose either:
   - **main** branch, **/docs** folder, or
   - **gh-pages** branch, **/(root)**
4. Save, wait 1–2 minutes, then open https://anjilrita-art.github.io/menote/

Share only this link — not `127.0.0.1` and not the raw HTML file.

## Option 2 — Render (uploads + API)

1. https://dashboard.render.com/select-repo?type=blueprint
2. Connect **menote** → **Apply**
3. Share the `https://studyhub-xxxx.onrender.com` URL

Free tier sleeps when idle; first visit may take ~30 seconds.

## Optional auto-redeploy (Render)

After creating the Render service: **Settings → Deploy Hook** → add URL as GitHub secret `RENDER_DEPLOY_HOOK_URL`.
