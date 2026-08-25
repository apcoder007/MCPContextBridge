"""Application entry point.

Run with:

    python -m mcp_server
"""

from pathlib import Path
import sys
import uvicorn



# Add src/ to Python's import path when running this file directly.
SRC_DIR = Path(__file__).resolve().parents[1]

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mcp_server.app.server import app


def main() -> None:
    """Start the MCP gateway."""

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )


if __name__ == "__main__":
    main()