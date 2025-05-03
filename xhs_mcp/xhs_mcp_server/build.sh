#!/bin/bash
set -e

IMAGE_NAME="${IMAGE_NAME:-xhs_mcp_server_image}"
CONTAINER_NAME="${CONTAINER_NAME:-xhs_mcp_server}"
ENV_FILE="${ENV_FILE:-.env}"
PORT="${MCP_HTTP_PORT:-8809}"

if [ -f "${ENV_FILE}" ]; then
  # shellcheck disable=SC1090
  set -a
  . "${ENV_FILE}"
  set +a
  PORT="${MCP_HTTP_PORT:-${PORT}}"
else
  echo "Missing ${ENV_FILE}. Please copy .env.example to .env and fill in XHS_COOKIE." >&2
  exit 1
fi

docker build -t "${IMAGE_NAME}" .
docker run -d --name "${CONTAINER_NAME}" \
  --restart unless-stopped \
  -p "${PORT}:${PORT}" \
  --env-file "${ENV_FILE}" \
  "${IMAGE_NAME}" \
  uv --directory /app run main.py --type sse --port "${PORT}"
