# ---------- Base image ----------
FROM python:3.12-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ---------- Working directory ----------
WORKDIR /app

# ---------- System dependencies ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- Python dependencies ----------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Application code ----------
COPY . .

# ---------- Non-root user ----------
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# ---------- Expose port ----------
EXPOSE 8000

# ---------- Healthcheck ----------
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# ---------- Run ----------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]