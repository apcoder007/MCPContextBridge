# MCPContextBridge
Production-ready Python MCP server platform for AI agents. Provides modular tools, multiple MCP servers, Streamable HTTP transport, configurable endpoints, and integrations with external services. Designed for scalable, secure, observable, and maintainable MCP deployments.

python src/mcp_server/__main__.py

## Langfuse tracing

MCP tool executions are traced with Langfuse when its credentials are
configured. Add these variables to `.env`:

```text
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
```

The calculator and GitHub MCP tools are traced individually. GitHub access
tokens are resolved inside the tool implementation and are not passed to
Langfuse as trace inputs.
