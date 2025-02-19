FROM ghcr.io/chroma-core/chroma:0.6.3

RUN apt-get update && apt-get install -y \
    iputils-ping \
    net-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*
