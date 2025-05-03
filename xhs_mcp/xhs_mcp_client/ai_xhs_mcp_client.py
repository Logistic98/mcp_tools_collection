# -*- coding: utf-8 -*-

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

load_dotenv()

VLLM_BASE = os.getenv("VLLM_BASE")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
MCP_SSE_URL = os.getenv("MCP_SSE_URL", "http://localhost:8809/sse")

if not VLLM_BASE:
    raise RuntimeError("VLLM_BASE is required. Set it in .env or environment variables.")
if not API_KEY:
    raise RuntimeError("API_KEY is required. Set it in .env or environment variables.")

client = OpenAI(base_url=VLLM_BASE, api_key=API_KEY)


def mcp_tools_to_openai_tools(tools):
    openai_tools = []
    for t in tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": t.name,
                "description": getattr(t, "description", "") or "",
                "parameters": getattr(t, "inputSchema", None) or {
                    "type": "object",
                    "properties": {}
                }
            }
        })
    return openai_tools


async def run():
    async with sse_client(MCP_SSE_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            lst = await session.list_tools()
            tools = lst.tools
            openai_tools = mcp_tools_to_openai_tools(tools)

            messages = [
                {"role": "system", "content": "You are a helpful assistant that can use tools via function calling."},
                {"role": "user", "content": "用小红书工具搜索‘大理旅游’，返回点赞量最多的5条帖子，以JSON格式输出，每条帖子包含标题、链接和点赞量。"}
            ]

            while True:
                # 调用 LLM（OpenAI chat.completions）
                resp = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    tools=openai_tools,
                    tool_choice="auto"
                )

                if not resp or not getattr(resp, "choices", None):
                    print("LLM 没有返回有效结果:", resp)
                    break

                choice = resp.choices[0]
                msg = choice.message
                messages.append({
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": msg.tool_calls
                })

                # 如果有工具调用
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        fn = tc.function.name
                        args = json.loads(tc.function.arguments or "{}")
                        print(f"\n[LLM] 触发工具调用: {fn}  参数={args}")

                        # 调用 MCP 工具
                        result = await session.call_tool(fn, args)

                        tool_content = []
                        for c in result.content:
                            if hasattr(c, "text"):
                                tool_content.append(c.text)
                            else:
                                tool_content.append(json.dumps(c.__dict__, ensure_ascii=False))
                        tool_output = "\n".join(tool_content) if tool_content else "OK"

                        print(f"[MCP] 工具返回结果:\n{tool_output}\n")

                        # 把结果加回消息流
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "name": fn,
                            "content": tool_output
                        })

                    print("[SYSTEM] 工具调用完成 → 进入下一轮推理\n")
                    continue

                # 没有工具调用，直接输出答案
                print("\n[LLM 最终回答]\n", msg.content)
                break


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
