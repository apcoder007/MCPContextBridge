from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

from mcp_server.tools.generic.calculator import register as register_calculator
from mcp_server.tools.github.tools import register as register_github

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
# GitHub MCP server
# ---------------------------------------------------------

github_mcp = FastMCP(
    name="GitHub",
    instructions="""
    This MCP server provides read-only access to GitHub repositories
    using the GitHub API.

    Use the GitHub tools whenever the user asks about GitHub
    repositories, files, issues, commits, branches, repository
    status, or recent changes.

    Available capabilities include:

    - Get repository information
    - List repository issues
    - Read files from a repository
    - Get recent commits
    - Get repository status
    - Get the latest change or commit

    Repository identification:

    - Always identify the repository using its GitHub owner and
      repository name.
    - The owner may be a GitHub username or organization name.
    - Do not assume the owner or repository name when it is not
      provided or cannot be determined from the conversation.

    Tool usage:

    - Use github_repository when the user asks for repository
      information or metadata.
    - Use github_issues when the user asks about repository issues.
    - Use github_file when the user asks to read a file from a
      repository.
    - Use github_commits when the user asks for commit history or
      recent commits.
    - Use github_status when the user asks for the current
      repository status, default branch, or latest commit.
    - Use github_last_change when the user asks what changed most
      recently or asks for the latest change.

    GitHub authentication:

    - Authentication is handled by the server using the
      GITHUB_PERSONAL_ACCESS_TOKEN environment variable.
    - Never ask the user to provide their PAT in a tool argument.
    - Never expose, return, log, or include the PAT in tool output.

    Accuracy:

    - Always use the GitHub tools to retrieve current repository
      information instead of relying on previously known information.
    - Do not invent repository names, branches, commits, issues,
      files, or GitHub metadata.
    - If a GitHub API request fails, report the relevant error
      without exposing credentials.

    Scope:

    - Use these tools for GitHub-related requests.
    - Do not use GitHub tools for unrelated arithmetic,
      filesystem, or general-purpose tasks.
    """,
)

register_github(github_mcp)

# ---------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: Starlette):
    """Manage the lifecycle of all MCP servers."""

    async with (
        calculator_mcp.session_manager.run(),
        github_mcp.session_manager.run(),
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
        Mount(
            "/github",
            app=github_mcp.streamable_http_app(),
        ),
    ],
    lifespan=lifespan,
)