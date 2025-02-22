FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic1 \
    file \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (to leverage Docker layer caching)
COPY requirements/backend_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r backend_requirements.txt

# Download all necessary NLTK data
RUN python -m nltk.downloader -d /usr/local/share/nltk_data all
# Alternatively, if you want to download only specific packages:
# RUN python -c "import nltk; \
#     nltk.download('punkt', download_dir='/usr/local/share/nltk_data'); \
#     nltk.download('averaged_perceptron_tagger', download_dir='/usr/local/share/nltk_data'); \
#     nltk.download('punkt_tab', download_dir='/usr/local/share/nltk_data'); \
#     nltk.download('tokenizers', download_dir='/usr/local/share/nltk_data')"

# Set environment variable for NLTK data
ENV NLTK_DATA=/usr/local/share/nltk_data

# Copy application code
COPY backend /app/backend

# Create necessary directories
RUN mkdir -p /app/documents /app/vector_store

# Set permissions for appuser
RUN useradd -m appuser && \
    chown -R appuser:appuser /app/documents && \
    chown -R appuser:appuser /app/vector_store && \
    chown -R appuser:appuser /app/backend && \
    chown -R appuser:appuser /usr/local/share/nltk_data

# Switch to non-root user
USER appuser

# Set the working directory inside backend
WORKDIR /app/backend

# Expose the port
EXPOSE 8000

# Run the backend
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]