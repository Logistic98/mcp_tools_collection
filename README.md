## MCP Tools Collection

本仓库包含两个 MCP 工具示例：Bocha 搜索 MCP 与小红书 MCP。

每个模块分为 server 与 client，便于本地运行、Docker 部署和模型工具调用集成。

## 项目结构

```text
.
├── bocha_mcp/
│   ├── bocha_mcp_client/
│   └── bocha_mcp_server/
└── xhs_mcp/
    ├── xhs_mcp_client/
    └── xhs_mcp_server/
```

## 环境变量与敏感信息

初始化配置时，请复制对应目录下的 `.env.example`：

```bash
cp bocha_mcp/bocha_mcp_server/.env.example bocha_mcp/bocha_mcp_server/.env
cp bocha_mcp/bocha_mcp_client/.env.example bocha_mcp/bocha_mcp_client/.env
cp xhs_mcp/xhs_mcp_server/.env.example xhs_mcp/xhs_mcp_server/.env
cp xhs_mcp/xhs_mcp_client/.env.example xhs_mcp/xhs_mcp_client/.env
```

然后根据本地实际环境填写 `.env`。请勿将真实 `.env`、API Key、Cookie 或访问令牌提交到 Git。

## 快速启动

### Bocha MCP Server

```bash
cd bocha_mcp/bocha_mcp_server
cp .env.example .env
uv sync
uv run bocha-search-mcp
```

或使用 Docker：

```bash
bash build.sh
```

### XHS MCP Server

```bash
cd xhs_mcp/xhs_mcp_server
cp .env.example .env
uv sync
uv run python main.py --type sse --port 8809
```

或使用 Docker：

```bash
bash build.sh
```

### MCP Client 示例

```bash
cd bocha_mcp/bocha_mcp_client
cp .env.example .env
uv sync
uv run python bocha_mcp_client.py

cd ../../xhs_mcp/xhs_mcp_client
cp .env.example .env
uv sync
uv run python xhs_mcp_client.py
```
