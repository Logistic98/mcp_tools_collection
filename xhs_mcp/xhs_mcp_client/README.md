# XHS MCP Client

XHS MCP Client 是一个基于 **Model Context Protocol (MCP)** 协议的轻量级客户端，  
用于与 XHS MCP Server 建立 SSE 长连接，并通过标准接口调用小红书相关工具（如笔记搜索、评论获取等）。

---

## 🚀 功能概述

该客户端支持以下能力：

- 建立与 XHS MCP Server 的 **SSE 长连接**；
- 自动加载与发现服务端可用工具；
- 执行如 `search_notes`、`get_note_content` 等接口；
- 输出结构化结果，可直接用于大模型上下文扩展。

---

## ⚙️ 环境要求

- Python ≥ 3.11  
- 已启动的 XHS MCP Server（端口默认为 8809）  

安装依赖：

```bash
pip install -r requirements.txt
```

或使用 `pyproject.toml`：

```bash
uv pip install --system -r pyproject.toml
```

---

## 🧩 使用方法

运行示例：

```bash
cp .env.example .env
python xhs_mcp_client.py
```

输出示例：

```
=== 已连接 XHS MCP 服务 ===
可用工具: ['check_cookie', 'search_notes', 'get_note_content', 'get_note_comments']

执行 search_notes 搜索 “大理旅游”
返回结果:
Title: 大理3日游路线推荐
URL: https://www.xiaohongshu.com/explore/...
Likes: 15300
```

---

## 💡 与 Qwen3 结合使用

`ai_xhs_mcp_client.py` 提供了自动工具调用示例：

```bash
cp .env.example .env
# edit .env and set VLLM_BASE / API_KEY
python ai_xhs_mcp_client.py
```

模型会自动识别意图并调用相应 MCP 工具，例如：

```
[LLM] -> 调用 search_notes 参数: {'keywords': '护肤推荐'}
[MCP] -> 返回 10 条笔记摘要
```

