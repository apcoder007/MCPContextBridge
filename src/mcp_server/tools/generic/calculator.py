from decimal import Decimal, InvalidOperation
from typing import Literal

from langfuse import observe
from mcp.server.fastmcp import FastMCP

from mcp_server.observability import update_tool_input

Operation = Literal[
    "add",
    "subtract",
    "multiply",
    "divide"
]

def calculate(
        operation: Operation,
        a: Decimal,
        b: Decimal
) -> Decimal:
    """Perform a mathematical operation."""

    match operation:
        case "add":
            return a + b
        case "subtract":
            return a - b
        case "multiply":
            return a * b
        case "divide":
            if b == 0:
                raise ValueError("Division by zero is not allowed")
            return a / b
        case _:
            raise ValueError(
                f"Unsupported operation: {operation}"
            )

def register(mcp: FastMCP) -> None:
    """Register calculator MCP tools."""

    @mcp.tool()
    @observe(
        name="calculator",
        as_type="tool",
        capture_input=True,
        capture_output=True,
    )
    async def calculator(
        operation: Operation,
        a: float,
        b: float,
    ) -> dict[str, str]:
        """Perform arithmetic calculations.

            Use this tool whenever the user asks to perform arithmetic
            or calculate a numerical result.

            This includes natural-language requests such as:
            - add 7 and 9
            - what is 7 plus 9
            - calculate 7 + 9
            - multiply 7 by 9
            - subtract 9 from 20
            - divide 20 by 5

            Do not perform arithmetic yourself when this tool is available.

            Args:
                operation: One of add, subtract, multiply, or divide.
                a: First number.
                b: Second number.

            Returns:
                The calculated numeric result.
        """

        update_tool_input({
            "operation": operation,
            "a": a,
            "b": b,
        })

        try:
            left = Decimal(str(a))
            right = Decimal(str(b))

            result = calculate(
                operation=operation,
                a=left,
                b=right,
            )

            return {
                "operation": operation,
                "a": str(left),
                "b": str(right),
                "result": str(result),
            }

        except (InvalidOperation, ValueError) as exc:
            raise ValueError(str(exc)) from exc