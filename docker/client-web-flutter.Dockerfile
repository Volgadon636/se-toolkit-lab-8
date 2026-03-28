# Flutter web client for Task 2 — build context is the repo root (see docker-compose.yml).
# Uses ghcr.io/cirruslabs/flutter directly so Harbor/ghcr proxy is not required for the builder stage.

ARG REGISTRY_PREFIX_DOCKER_HUB

FROM ghcr.io/cirruslabs/flutter:3.41.2 AS builder

WORKDIR /app

COPY nanobot-websocket-channel/client-web-flutter/pubspec.yaml nanobot-websocket-channel/client-web-flutter/pubspec.lock ./
RUN --mount=type=cache,target=/root/.pub-cache flutter pub get

COPY nanobot-websocket-channel/client-web-flutter/ .
RUN --mount=type=cache,target=/app/.dart_tool \
    flutter build web --base-href /flutter/

FROM ${REGISTRY_PREFIX_DOCKER_HUB}alpine:3.21
COPY --from=builder /app/build/web /flutter-web
CMD ["cp", "-r", "/flutter-web/.", "/output/"]
