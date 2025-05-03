from bocha_search_mcp.server import server
import os
import sys

def main():
    """Initialize and run the Bocha Search MCP server (SSE mode)."""

    if "BOCHA_API_KEY" not in os.environ:
        print("Error: BOCHA_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    host = os.environ.get("MCP_HTTP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_HTTP_PORT", "8810"))

    print(f"Starting Bocha Search MCP server on {host}:{port} (SSE mode)...", file=sys.stderr)

    server.run(transport="sse", host=host, port=port)

__all__ = ["main", "server"]
