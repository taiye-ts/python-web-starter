FROM python:3.8.1-alpine3.10

ENV PYTHONUNBUFFERED 1

# Application packages
RUN apk add --no-cache  --virtual .run-deps \
        vim \
        zlib-dev \
        postgresql \
        postgresql-dev \
        libxml2-dev \
        libxslt-dev \
    && mkdir -p /app \
    && mkdir -p /app/requirements

# ENVIRONMENT - "prod" or "dev"
ARG PROJECT_ENVIRONMENT=dev

COPY env/requirements /app/requirements

# Build packages
RUN apk add --no-cache  --virtual .build-deps \
        gcc \
        musl-dev \
        linux-headers \
    && rm -rf /var/cache/apk/* \
    && pip install --upgrade pip==19.3.1 \
    && pip install --no-cache-dir -r /app/requirements/${PROJECT_ENVIRONMENT}.txt \
    && apk del .build-deps

WORKDIR /app

# Copy project files
COPY src /app

ENV PYTHONPATH="/app:${PATH}"
