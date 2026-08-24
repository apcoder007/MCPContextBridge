from mcp.server.fastmcp import FastMCP

from mcp_server.tools.generic import calculator

def register_tools(mcp: FastMCP) -> None:
    """Register all MCP tools."""

    calculator.register(mcp)