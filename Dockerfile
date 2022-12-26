FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get -y install libpq-dev
RUN apt-get -y install build-essential

RUN useradd --create-home --shell /bin/bash worker
USER worker

WORKDIR /opt/app

# Add pipx installed binaries to PATH
ENV PATH="/home/worker/.local/bin:${PATH}"

# Install dependencies
RUN pip install pipx && \
    pipx install poetry && \
    pipx install virtualenv

RUN virtualenv .venv

# Activate virtual environment
ENV VIRTUAL_ENV="/opt/app/.venv" \
    PATH="/opt/app/.venv/bin:$PATH"

COPY pyproject.toml /opt/app/

RUN poetry install

# Set variables for pytest only
ENV PYTHONUNBUFFERED=1 \
    PYTHONDEVMODE=1 \
    PYTHONDONTWRITEBYTECODE=1
