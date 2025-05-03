# Bocha MCP Server

Bocha MCP Server 是基于 **FastMCP** 框架实现的 **MCP 服务端工具集**，用于封装 Bocha 搜索接口，提供统一的模型上下文扩展能力。  
服务以 **SSE 模式** 运行，支持直接通过 MCP 客户端访问。

---

## 🚀 功能概述

Bocha MCP Server 提供以下工具：

### 1. `bocha_web_search`

基于 Bocha Web Search API 的网页搜索工具，可获取网页标题、URL、摘要、发布日期及站点信息。

### 2. `bocha_ai_search`

调用 Bocha AI Search API，具备语义识别与结构化卡片返回能力，适用于垂直领域内容搜索。

---

## ⚙️ 环境要求

- Python ≥ 3.12  
- 环境变量配置（推荐使用 `.env` 文件）：

```bash
BOCHA_API_KEY=your_bocha_api_key
MCP_HTTP_HOST=0.0.0.0
MCP_HTTP_PORT=8810
```

可参考 `.env.example` 文件。

依赖包（见 `pyproject.toml`）：

```toml
mcp[cli]>=1.6.0
fastmcp>=0.4.0
httpx>=0.27.0
python-dotenv>=1.0.1
```

---

## 🧩 启动服务

### 方式一：本地运行

```bash
cp .env.example .env
# edit .env and set BOCHA_API_KEY
python -m bocha_search_mcp
```

输出示例：

```
Starting Bocha Search MCP server on 0.0.0.0:8810 (SSE mode)...
```

### 方式二：Docker 启动

项目内已包含 Dockerfile，可直接构建镜像：

```bash
docker build -t bocha-search-mcp .
docker run -d -p 8810:8810 --env-file .env bocha-search-mcp
```

---

## 📚 工具定义

每个工具均通过 `@server.tool()` 装饰器定义，返回纯文本结果。  
调用逻辑示例（以 `bocha_web_search` 为例）：

```python
@server.tool()
async def bocha_web_search(query: str, freshness: str = "noLimit", count: int = 10) -> str:
    ...
    endpoint = "https://api.bochaai.com/v1/web-search"
    payload = {"query": query, "summary": True, "count": count}
    ...
```

结果格式包括：

- Title  
- URL  
- Description  
- Published date  
- Site name  

---

## 🧱 运行机制

服务使用 `FastMCP` 实现：

- `server.run(transport="sse", host, port)` 启动 SSE 服务；
- 客户端通过 MCP SSE 协议连接；
- 所有工具动态注册并可通过 `session.list_tools()` 发现。
