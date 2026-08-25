from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

from mcp_server.tools.generic import register as register_calculator

# ---------------------------------------------------------
# Calculator MCP server
# ---------------------------------------------------------

calculator_mcp = FastMCP(
    name="Calculator",
    instructions="""
    Calculator MCP server.

    Use the calculator tool whenever the user asks
    to perform arithmetic calculations.
    """,
)

register_calculator(calculator_mcp)

# ---------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: Starlette):
    """Manage the lifecycle of all MCP servers."""

    async with (
        calculator_mcp.session_manager.run(),
        # github_mcp.session_manager.run(),
    ):
        yield

# ---------------------------------------------------------
# Mount MCP servers
# ---------------------------------------------------------

app = Starlette(
    routes=[
        Mount(
            "/calculator",
            app=calculator_mcp.streamable_http_app(),
        ),
        # Mount(
        #     "/github",
        #     app=github_mcp.streamable_http_app(),
        # ),
    ],
    lifespan=lifespan,
)