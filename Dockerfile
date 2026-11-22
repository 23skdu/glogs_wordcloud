# syntax=docker/dockerfile:1
# Build stage
FROM python:3.15.2-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential=12.9 gcc=4:12.2.0-3 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/venv/bin/pip install .

# Runtime stage
FROM python:3.15.2-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}"

# Runtime system dependencies for matplotlib/wordcloud fonts
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends fonts-dejavu-core=2.37-6 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /app --create-home app

COPY --from=builder /opt/venv /opt/venv

# Upgrade vulnerable transitive system packages in the runtime image.
RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade "setuptools>=78.1.1" \
    && rm -rf /root/.cache/pip

WORKDIR /app
USER 10001:10001

ENTRYPOINT ["glogs-wordcloud"]
CMD ["--help"]