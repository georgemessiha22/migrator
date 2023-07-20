FROM python:3.12.0b4-alpine3.18 as base

LABEL maintainer="George Messiha <georgemessiha22@gmail.com>"

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"

ENV POETRY_VIRTUALENVS_CREATE=false

COPY ./dev/docker/entrypoint /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint

# install awesome poetry & postgres driver
RUN apk add poetry libpq postgresql-dev mysql-client

FROM base as dev

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN poetry install

# ENTRYPOINT ["sh", "/usr/local/bin/entrypoint"]

#create a non root user to access the container
RUN adduser --uid 5678 --disabled-password --gecos "" editor

FROM base as release

# get the build version from docker build args, default value set to version 0.0.0
ARG build_version="v0.0.0"
# we reference it directly, so every container of this image has the version provided
ENV VERSION=$build_version

COPY ./migrator /app/migrator

WORKDIR /app

COPY ./pyproject.toml /app/pyproject.toml

RUN poetry install --only main --compile --no-interaction

ENTRYPOINT ["sh", "/usr/local/bin/entrypoint"]

CMD ["sh", "migrator", "migrate"]
