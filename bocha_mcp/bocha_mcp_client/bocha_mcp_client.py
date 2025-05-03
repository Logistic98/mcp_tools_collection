# -*- coding: utf-8 -*-

"""
Bocha Search MCP SSE 客户端示例
"""

import asyncio
import os
from dotenv import load_dotenv
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession


load_dotenv()

MCP_SSE_URL = os.getenv("MCP_SSE_URL", "http://127.0.0.1:8810/sse")


async def main():
    """连接 Bocha MCP 服务器并调用搜索工具"""

    try:
        async with sse_client(MCP_SSE_URL) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("已连接 Bocha Search MCP 服务")

                tools = await session.list_tools()
                tool_names = [t.name for t in tools.tools]
                print("可用工具：", tool_names)

                if "bocha_web_search" not in tool_names:
                    print("未发现 bocha_web_search 工具，请确认服务端已加载该工具。")
                    return

                query = "Agent 技术趋势"
                print(f"\n正在调用 bocha_web_search 搜索: {query}\n")

                result = await session.call_tool(
                    "bocha_web_search",
                    {"query": query, "count": 3}
                )

                print("搜索结果:\n")
                for content in result.content:
                    text = getattr(content, "text", str(content))
                    print(text)
                    print("-" * 80)

    except ConnectionRefusedError:
        print("无法连接到 Bocha MCP SSE 服务，请确认服务端已运行。")
    except asyncio.TimeoutError:
        print("连接 MCP SSE 服务超时，请检查网络或防火墙。")
    except Exception as e:
        print(f"出现错误：{type(e).__name__}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
