# XHS MCP Server

XHS MCP Server 是基于 **FastMCP** 框架实现的小红书数据工具服务，通过 MCP 协议封装了小红书 Web API，支持笔记搜索、内容提取、评论抓取等能力。 该服务可以通过本地或 Docker 容器快速启动，并支持被任意 MCP 客户端调用。

---

## 🚀 功能概述

核心功能包括：

- ✅ **check_cookie**：检测 Cookie 是否有效  
- 🔍 **search_notes**：搜索笔记  
- 📄 **get_note_content**：获取笔记标题、正文、图片、标签  
- 💬 **get_note_comments**：抓取评论列表  
- ✏️ **post_comment**：发表评论  
- 🏠 **home_feed**：获取首页推荐流内容  

---

## ⚙️ 环境要求

- Python ≥ 3.12  
- Node.js ≥ 18（用于签名脚本执行）  
- 环境变量：

```bash
XHS_COOKIE=your_xiaohongshu_cookie
MCP_HTTP_PORT=8809
```

依赖定义（见 `pyproject.toml`）：

```toml
mcp[cli]>=1.6.0
fastmcp>=0.4.0
curl-cffi>=0.7.0
requests>=2.32.0
pyexecjs>=1.5.1
```

---

## 🧩 启动方式

### 方式一：本地启动

```bash
cp .env.example .env
# edit .env and set XHS_COOKIE
python main.py --type sse --port 8809
```

输出示例：

```
Starting XHS MCP Server on 0.0.0.0:8809 (SSE mode)...
```

### 方式二：Docker 启动

```bash
docker build -t xhs-mcp-server .
docker run -d -p 8809:8809 --env-file .env xhs-mcp-server
```

或直接运行 `build.sh`：

```bash
bash build.sh
```

---

## 🔒 签名机制说明

小红书请求需携带 `X-s` 与 `X-t` 签名。  
服务端内置 `api/xhsvm.js`，通过 `execjs` 调用 JavaScript 代码生成签名字段。  
无需手动计算，调用 API 时会自动注入。

---

## 🧱 服务架构

- 使用 **FastMCP** 实现服务注册与工具暴露；
- 自动注册所有 `@mcp.tool()` 定义的方法；
- SSE 模式下支持多客户端并发连接；
- 日志与错误信息通过标准输出返回。
