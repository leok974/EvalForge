FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (Cloud Run will set PORT env var)
EXPOSE 8080

# Start FastAPI with uvicorn (includes all routes: ADK + DevDiag proxy)
CMD ["sh", "-c", "python -m uvicorn arcade_app.agent:app --host 0.0.0.0 --port ${PORT:-8080}"]