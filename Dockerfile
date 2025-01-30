FROM ghcr.io/chroma-core/chroma:0.6.3

# USER root

RUN apt-get update && apt-get install -y \
    iputils-ping \
    net-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*

# RUN mkdir -p /chroma/my_db && chown -R chromadb:chromadb /chroma/my_db

# USER chromadb