FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies needed by Pillow/onnxruntime/rembg
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libgl1 \
       libglib2.0-0 \
       libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080

# Run the Flask WSGI app via gunicorn
CMD ["gunicorn", "api.remove_bg:app", "-b", "0.0.0.0:8080", "--workers", "1", "--threads", "4"]
