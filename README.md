# Background Remover (Python + Vercel Serverless)

This project provides a simple open-source background remover using `rembg` and a small Flask-based serverless function deployable to Vercel.

Contents
- `api/remove_bg.py` — Serverless Flask function using `rembg` to remove image backgrounds.
- `index.html` — Frontend UI for uploading images and getting results.
- `requirements.txt` — Python dependencies.
- `vercel.json` — Vercel configuration.

Quick project structure
```
BGREMOVER/
├─ api/remove_bg.py
├─ index.html
├─ requirements.txt
├─ vercel.json
└─ README.md
```

Features
- Uses open-source `rembg` (no paid APIs).
- Single-image and batch processing (ZIP output for multiple images).
- File size limit: 10 MB per file (configurable in `remove_bg.py`).
- Basic error handling and friendly frontend instructions.

Notes about Vercel and dependency size
-------------------------------------
`rembg` depends on `onnxruntime` and downloads the `u2net` model the first time it runs. Vercel serverless functions have limits on package size and disk usage. If you run into deployment errors due to function size, consider:

- Using a smaller runtime / lighter library.
- Hosting the model on an external storage and loading it at runtime (advanced).
- Using a server or container service (Render, Railway, Fly, or Vercel's serverless with a custom build if permitted).

Deployment (step-by-step)
-------------------------
1. Install the Vercel CLI (if you don't have it):

```powershell
npm i -g vercel
```

2. From your project root (`BGREMOVER`), login to Vercel:

```powershell
vercel login
```

Follow the prompts.

3. (Optional local test) Create a Python virtualenv, install dependencies and run the app locally:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Run dev server for local testing (the Flask app listens on port 3000 when run directly)
python api\remove_bg.py
```

Then open `http://localhost:3000/` and POST to `/api/remove_bg` with a file (the local run is just for dev/testing).

4. Deploy to Vercel from project root:

```powershell
vercel --prod
```

Follow the prompts to select your project and confirm settings. Vercel will:
- Install dependencies from `requirements.txt` for the Python function
- Deploy static `index.html`
- Create serverless endpoint at `https://<your-vercel>.vercel.app/api/remove_bg`

5. Open the deployed site URL given by Vercel.

Business-ready considerations
----------------------------
- File size: `MAX_CONTENT_LENGTH` is set to 10 MB in `api/remove_bg.py`. Change `app.config['MAX_CONTENT_LENGTH']` to adjust.
- Error handling: API returns JSON errors with helpful messages and HTTP status codes.
- Beginner-friendly: `index.html` contains step-by-step instructions and friendly UI.

If you need production hardening
--------------------------------
- Add authentication, rate-limiting, and API usage logging.
- Use persistent model caching outside serverless runtime to reduce cold-start overhead.
- If package size exceeds Vercel limits, consider hosting the service on a container-friendly host (e.g., Docker on Render or Fly) or split the service: static frontend on Vercel and a separate Python service for background removal.

Contact
-------
If you'd like, I can:
- Add a small GitHub Actions pipeline to auto-deploy on push.
- Replace `rembg` with a lighter footprint option or adapt for GPU runtimes.
- Add tests and a small CI job to validate the function.

