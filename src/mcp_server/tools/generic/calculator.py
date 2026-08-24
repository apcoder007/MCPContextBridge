from decimal import Decimal, InvalidOperation
from typing import Literal

from mcp.server.fastmcp import FastMCP

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
    async def calculator(
        operation: Operation,
        a: float,
        b: float,
    ) -> dict[str, str]:
        """Perform a basic mathematical calculation.

        Args:
            operation: One of add, subtract, multiply, or divide.
            a: First number.
            b: Second number.

        Returns:
            A result object containing the operation and result.
        """

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