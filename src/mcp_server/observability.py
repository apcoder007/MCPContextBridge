"""Langfuse initialization and lifecycle helpers."""

from pathlib import Path

from dotenv import load_dotenv
from langfuse import get_client


load_dotenv(Path(__file__).with_name(".env"))

langfuse = get_client()


def update_tool_input(input_data: dict) -> None:
    """Set the structured input displayed for the active tool observation."""

    langfuse.update_current_span(input=input_data)


def flush() -> None:
    """Send queued Langfuse events before the process exits."""

    langfuse.flush()