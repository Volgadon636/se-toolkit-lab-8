# Stage 1: build the application in the `/app` directory.
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY --from=workspace pyproject.toml uv.lock /app/
COPY pyproject.toml /app/nanobot/pyproject.toml
COPY --from=workspace mcp/mcp-lms/pyproject.toml /app/mcp/mcp-lms/pyproject.toml
COPY --from=workspace mcp/mcp-obs/pyproject.toml /app/mcp/mcp-obs/pyproject.toml
COPY --from=workspace nanobot-websocket-channel/nanobot-webchat/pyproject.toml /app/nanobot-websocket-channel/nanobot-webchat/pyproject.toml
COPY --from=workspace nanobot-websocket-channel/mcp-webchat/pyproject.toml /app/nanobot-websocket-channel/mcp-webchat/pyproject.toml
COPY --from=workspace nanobot-websocket-channel/nanobot-channel-protocol/pyproject.toml /app/nanobot-websocket-channel/nanobot-channel-protocol/pyproject.toml

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

COPY . /app/nanobot
COPY --from=workspace mcp /app/mcp
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# Stage 2: final image
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

ARG APP_UID=1000
ARG APP_GID=1000

RUN if [ "${APP_UID}" != "0" ]; then \
    groupadd --system --gid ${APP_GID} nanobot \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home nanobot \
    && chown -R nanobot:nanobot /app; \
    fi

COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER ${APP_UID}
WORKDIR /app

CMD ["python", "nanobot/entrypoint.py"]
