from mcp.server.fastmcp import FastMCP

from mcp_server.tools.registry import register_tools
from mcp_server.config.settings import settings


mcp = FastMCP(
    name=settings.app_name,
    json_response=True
)

register_tools(mcp)