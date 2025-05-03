# -*- coding: utf-8 -*-

"""
MCP SSE 客户端测试
"""

import asyncio
import json
import os
import re
from dotenv import load_dotenv
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

load_dotenv()

MCP_SSE_URL = os.getenv("MCP_SSE_URL", "http://localhost:8809/sse")
TEST_NOTE_URL = os.getenv("TEST_NOTE_URL")


def print_result(tag, result):
    print(f"\n=== {tag} ===")
    if not result or not result.content:
        print("无返回")
        return
    for c in result.content:
        if hasattr(c, "text"):
            print(c.text)
        else:
            print(json.dumps(c.__dict__, ensure_ascii=False))


def extract_note_id(url: str):
    """从小红书笔记URL提取 note_id"""
    m = re.search(r"/explore/([0-9a-f]+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/discovery/item/([0-9a-f]+)", url)
    if m:
        return m.group(1)
    return None


async def main():
    async with sse_client(MCP_SSE_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("\n=== 握手成功 ===")

            # 打印服务端工具列表
            tools = await session.list_tools()
            print("\n=== 服务端提供的工具 ===")
            print(tools)

            # 1. 检查 cookie
            res = await session.call_tool("check_cookie", {})
            print_result("check_cookie", res)

            # 2. 搜索笔记
            res = await session.call_tool("search_notes", {"keywords": "旅行"})
            print_result("search_notes", res)

            # 3. 测试笔记链接
            target_url = TEST_NOTE_URL
            if not target_url:
                print("未配置 TEST_NOTE_URL，跳过指定笔记内容和评论测试。")
                return
            note_id = extract_note_id(target_url)

            print(f"\n选中指定笔记 URL: {target_url}")
            print(f"提取到 note_id: {note_id}")

            # 4. 获取笔记内容
            res = await session.call_tool("get_note_content", {"url": target_url})
            print_result("get_note_content", res)

            # 5. 获取笔记评论
            res = await session.call_tool("get_note_comments", {"url": target_url})
            print_result("get_note_comments", res)

            # # 6. 发布评论
            # if note_id:
            #     res = await session.call_tool("post_comment", {
            #         "note_id": note_id,
            #         "comment": "xhs-mcp test"
            #     })
            #     print_result("post_comment", res)
            # else:
            #     print("\n无法提取 note_id，跳过 post_comment")


if __name__ == "__main__":
    asyncio.run(main())
