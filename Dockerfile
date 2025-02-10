# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Environment variables (override with --env-file or -e flags)
ENV LLM_API_KEY=ollama
ENV DEFAULT_DB_URI=sqlite:///Chinook.db
ENV LLM_BASE_URL=http://localhost:11434/v1
ENV LLM_MODEL=llama3.2:latest

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]