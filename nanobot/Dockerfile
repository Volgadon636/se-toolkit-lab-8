# Nanobot gateway + LMS MCP + webchat channel (Task 2)
# Build context: ./nanobot  |  additional_contexts: workspace = repo root
# Python 3.12: nanobot-ai + plugins are tested on 3.11–3.12; 3.14 can break at runtime.

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY --from=workspace mcp /app/mcp
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel
COPY . /app/nanobot

WORKDIR /app/nanobot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev \
    && test -x /app/nanobot/.venv/bin/nanobot

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LANG=C.UTF-8

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/nanobot/.venv/bin:$PATH"
ENV NANOBOT_VENV_PYTHON=/app/nanobot/.venv/bin/python
ENV NANOBOT_CLI=/app/nanobot/.venv/bin/nanobot
WORKDIR /app/nanobot

# Fail build if venv paths break across stages (common Docker footgun).
RUN /app/nanobot/.venv/bin/python -c "import nanobot; from nanobot.config.schema import Config; print('nanobot import ok')"

USER nonroot

CMD ["/app/nanobot/.venv/bin/python", "entrypoint.py"]
