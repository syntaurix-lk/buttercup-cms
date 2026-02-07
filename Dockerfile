# =============================================================================
# Dockerfile for Buttercup CMS Backend
# =============================================================================
# Multi-stage build for optimized production image

# -----------------------------------------------------------------------------
# Stage 1: Build Stage
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Production Stage
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS production

# Image metadata
LABEL maintainer="Buttercup Dev Team" \
    version="1.0.0" \
    description="Buttercup Home Page CMS Backend API"

# Runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    APP_HOME=/app \
    PATH="/opt/venv/bin:$PATH"

# Runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Set working directory
WORKDIR $APP_HOME

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY --chown=appuser:appgroup . .

# Create required directories
RUN mkdir -p uploads logs && \
    chown -R appuser:appgroup uploads logs

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 30001

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:30001/api/v1/health/live || exit 1

# Default startup command (overridden by docker-compose if needed)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30001"]

# -----------------------------------------------------------------------------
# Stage 3: Development Stage (optional)
# -----------------------------------------------------------------------------
FROM production AS development

USER root

# Install development-only tools
RUN pip install pytest pytest-asyncio httpx black isort flake8

USER appuser

# Development command with hot reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30001", "--reload"]
