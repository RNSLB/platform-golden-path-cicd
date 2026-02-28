# Multi-stage build for smaller final image

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Create non-root user first
RUN useradd -m -u 1000 appuser

# Copy dependencies from builder to appuser's home
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application
COPY --chown=appuser:appuser app.py .

# Switch to non-root user
USER appuser

# Ensure scripts are in PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Expose port
EXPOSE 8080

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "60", "app:app"]