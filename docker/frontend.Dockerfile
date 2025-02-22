FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements/frontend_requirements.txt .
RUN pip install --no-cache-dir -r frontend_requirements.txt

# Copy application code and Chainlit config
COPY frontend /app/frontend
COPY chainlit.md /app/chainlit.md

# Command to run the frontend
CMD ["chainlit", "run", "frontend/app.py", "--host", "0.0.0.0", "--port", "8505"]