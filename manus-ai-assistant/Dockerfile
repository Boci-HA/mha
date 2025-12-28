ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base:latest
FROM ${BUILD_FROM}

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install Python and dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Install Python dependencies with --break-system-packages flag
RUN pip install --no-cache-dir --break-system-packages \
    aiohttp==3.9.1 \
    requests==2.31.0

# Copy addon files
COPY main.py /app/
COPY manus_integration.py /app/
COPY requirements.txt /app/

# Install additional requirements
RUN pip install --no-cache-dir --break-system-packages -r /app/requirements.txt

# Set working directory
WORKDIR /app

# Use the s6-overlay init system
ENTRYPOINT ["/init"]

# Run the addon
CMD ["python3", "main.py"]
