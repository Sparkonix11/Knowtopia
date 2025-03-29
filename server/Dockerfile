FROM python:3.10

WORKDIR /app

COPY server/requirements.txt /app/

RUN apt-get update && apt-get install -y --no-install-recommends git && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    rm -rf /var/lib/apt/lists/*

COPY server /app

EXPOSE 5000

CMD ["python", "app.py"]
