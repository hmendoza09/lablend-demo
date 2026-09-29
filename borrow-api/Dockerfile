# ---------- base: dependencies + source code ----------
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
# Copy the dependency list first so this layer is cached when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ---------- test: Jenkins runs "docker build --target test" ----------
# If any pytest test fails, this build step fails, and the pipeline stops.
FROM base AS test
RUN pip install --no-cache-dir -r requirements-dev.txt
RUN python -m pytest -v

# ---------- production: what actually runs ----------
FROM base AS production
RUN useradd --create-home appuser
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
