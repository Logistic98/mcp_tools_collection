# =====================================
# Dockerfile for Bocha Search MCP (SSE)
# =====================================

FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml README.md ./
COPY src ./src
COPY .env.example .env

RUN uv pip install --system -U fastmcp>=0.4.0 httpx python-dotenv
RUN uv pip install --system -e .

ENV PYTHONPATH=/app/src
ENV MCP_HTTP_HOST=0.0.0.0
ENV MCP_HTTP_PORT=8810

CMD ["fastmcp", "run", "/app/src/bocha_search_mcp/server.py:server", "--transport", "sse", "--host", "0.0.0.0", "--port", "8810"]
