# Nanobot gateway — Task 2
# Build: docker compose build nanobot (context ./nanobot, additional_contexts workspace: .)

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=workspace mcp /app/mcp
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel
COPY . /app/nanobot

WORKDIR /app/nanobot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev \
    && test -x /app/nanobot/.venv/bin/nanobot

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LANG=C.UTF-8

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/nanobot/.venv/bin:$PATH"
ENV NANOBOT_VENV_PYTHON=/app/nanobot/.venv/bin/python
WORKDIR /app/nanobot

RUN /app/nanobot/.venv/bin/python -c "import nanobot; from nanobot.config.schema import Config; print('nanobot import ok')"

USER nonroot

CMD ["python", "/app/nanobot/entrypoint.py"]
