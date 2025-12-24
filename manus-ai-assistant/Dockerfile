ARG BUILD_FROM=ghcr.io/home-assistant/python-base:3.11

FROM ${BUILD_FROM}

# Install dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Install Python dependencies
RUN pip install --no-cache-dir \
    aiohttp==3.9.1 \
    requests==2.31.0

# Copy addon files
COPY main.py /app/main.py
COPY addon_config.json /app/addon_config.json

WORKDIR /app

# Run the addon
CMD [ "python3", "-u", "main.py" ]
