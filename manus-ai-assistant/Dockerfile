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
COPY main.py /
COPY manus_integration.py /
COPY requirements.txt /

# Install additional requirements
RUN pip install --no-cache-dir --break-system-packages -r /requirements.txt

# Run the addon directly
CMD ["python3", "/main.py"]
