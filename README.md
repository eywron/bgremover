# Background Remover (Python + Docker)

This project removes image backgrounds using the open-source `rembg` library and provides a small Flask API and a simple frontend. It is packaged for container deployment (Render, Fly, Railway, Docker).

Files
- `api/remove_bg.py` — Flask API using rembg. POST endpoint at `/api/remove_bg` (form field `file`). Added `/health` GET.
- `index.html` — Frontend UI.
- `Dockerfile` / `docker-compose.yml` — Container setup using Python 3.10-slim and Gunicorn.
- `requirements.txt` — Python deps (rembg, onnxruntime, Pillow, Flask, gunicorn).

Quick local test (without Docker)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python api\remove_bg.py
```
Open http://localhost:8080/ (for container mode) or if testing without Docker, the Flask app runs at port 8080.

Docker local test
```powershell
docker build -t bgremover:latest .
docker run --rm -p 3000:8080 bgremover:latest
```
Open http://localhost:3000 to use the UI.

Deploy to Render (Docker)
1. Push this repository to GitHub.
2. In Render dashboard, create a new Web Service -> Connect to your GitHub repo.
3. Select "Docker" as the environment (Render will use the `Dockerfile`). Set the service to listen on port `8080`.
4. Deploy. Render will build the Docker image and run it.

Notes
- The first time the server runs it will download the `u2net` model used by `rembg` — this increases startup time.
- If you need faster startup or lower memory, consider using a smaller model or hosting the model separately and loading it from persistent storage.

Restore from previous state
If you need the previous files (commits before the deletion), create a branch from the earlier commit SHA and push it.

