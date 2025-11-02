# =========================
# Stage 1: Build dependencies
# =========================
FROM python:3.13-slim AS builder

# Optimize Python environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies for compiled packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libmariadb-dev \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Optionally install Daphne for ASGI apps
RUN pip install --no-cache-dir daphne


# =========================
# Stage 2: Production image
# =========================
FROM python:3.13-slim

# Runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    libmariadb3 \
    netcat-traditional \
    libjpeg62-turbo \
    libpng16-16 \
    curl \
    && rm -rf /var/lib/apt/lists/* && apt-get clean

# Arguments for UID/GID and port
ARG USER_UID=1000
ARG USER_GID=1000
ARG APP_PORT=8000

# Create non-root user
RUN groupadd -r appuser -g ${USER_GID} && useradd -r -u ${USER_UID} -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application source code
COPY --chown=appuser:appuser . .

# Copy entrypoint script
COPY --chown=appuser:appuser entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    sed -i 's/\r$//' /entrypoint.sh

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_PORT=${APP_PORT}

# Switch to non-root user
USER appuser

# Expose port
EXPOSE ${APP_PORT}

# Entrypoint handles setup before starting server
ENTRYPOINT ["/entrypoint.sh"]

# Default command: use Gunicorn (WSGI). Change CMD for Daphne if needed.
CMD ["gunicorn", "--bind", "0.0.0.0", "-p", "$APP_PORT", "--workers", "3", "config.wsgi:application"]
