FROM python:3.10

# Set working directory
WORKDIR /app

# Copy only requirements first (to use caching)
COPY server/requirements.txt /app/

# Install dependencies in one layer (faster caching)
RUN apt-get update && apt-get install -y --no-install-recommends git && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the code
COPY server /app

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]