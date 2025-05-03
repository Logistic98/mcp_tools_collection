# Bocha MCP Client

Bocha MCP Client 是基于MCP 实现的轻量级客户端示例，用于通过 SSE（Server-Sent Events） 协议连接到 Bocha MCP Server，并调用其提供的搜索工具。

---

## 🚀 功能概述

该客户端主要功能：

- 与 Bocha MCP Server 建立 SSE 长连接；
- 自动加载可用工具；
- 调用 `bocha_web_search` 工具执行实时搜索；
- 解析与输出搜索结果。

示例默认连接到：

```
http://127.0.0.1:8810/sse
```

---

## ⚙️ 环境要求

- Python ≥ 3.11  
- 已启动的 Bocha MCP Server 实例（端口 8810）  

依赖包在 `pyproject.toml` 中定义，包括：

```toml
mcp[cli]>=1.6.0
openai>=1.102.0
python-dotenv>=1.1.1
```

安装方式：

```bash
pip install -r requirements.txt
# 或
uv pip install --system -r pyproject.toml
```

---

## 📖 使用方法

运行示例：

```bash
cp .env.example .env
python bocha_mcp_client.py
```

输出示例：

```
已连接 Bocha Search MCP 服务
可用工具： ['bocha_web_search', 'bocha_ai_search']

正在调用 bocha_web_search 搜索: Agent 技术趋势

搜索结果:
Title: ...
URL: ...
Description: ...
Published date: ...
Site name: ...
```

---

## 🧩 代码结构

- `bocha_mcp_client.py`：主执行文件；
- 使用 `mcp.client.sse.sse_client` 连接服务；
- 通过 `ClientSession` 调用工具。
