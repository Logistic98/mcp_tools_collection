#!/bin/bash
set -e

IMAGE_NAME="${IMAGE_NAME:-bocha-search-mcp-image}"
TAG="${TAG:-latest}"
CONTAINER_NAME="${CONTAINER_NAME:-bocha-search-mcp}"
ENV_FILE="${ENV_FILE:-.env}"

if [ ! -f "${ENV_FILE}" ]; then
  echo "Missing ${ENV_FILE}. Please copy .env.example to .env and fill in BOCHA_API_KEY." >&2
  exit 1
fi

echo "======================================"
echo "Building Docker image: $IMAGE_NAME:$TAG"
echo "======================================"

# 构建镜像
docker build -t ${IMAGE_NAME}:${TAG} .
echo "Build complete."

# 启动容器
echo "======================================"
echo "Running Bocha Search MCP container"
echo "======================================"
docker run -itd \
  --name ${CONTAINER_NAME} \
  -p 8810:8810 \
  --env-file "${ENV_FILE}" \
  ${IMAGE_NAME}:${TAG}
