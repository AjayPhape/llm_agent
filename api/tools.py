import json
import logging
from pydoc import Helper
from typing import Callable, Dict, List

from google.adk.tools import ToolContext
from google.adk.tools.toolbox_toolset import ToolboxToolset
from tabulate import tabulate

from config.llm import MCP_TOOLBOX_URL, MCP_TOOLSET
from db_agent.utils import PostgresDB
from schemas.db import HelperData

logger = logging.getLogger(__name__)


# In-memory todo storage


def add_todo(task: str, tool_context: ToolContext) -> dict:
    """Add a task to the todo list."""
    tmp_list = tool_context.state.get("to_do_list", [])
    tmp_list.append({"task": task, "done": False})

    tool_context.state["to_do_list"] = tmp_list

    return {
        "statusMessage": f"Added task: {task}",
        "to_do_list": tool_context.state["to_do_list"],
    }


def list_todos(tool_context: ToolContext) -> dict:
    """List all todo tasks."""
    tmp_list = tool_context.state.get("to_do_list", [])

    if not tmp_list:
        return {
            "statusMessage": "No tasks available",
            "to_do_list": tool_context.state["to_do_list"],
        }

    results = []

    for idx, todo in enumerate(tmp_list, start=1):
        status = "✅" if todo["done"] else "❌"
        results.append(f"{idx}. {status} {todo['task']}")

    return {
        "statusMessage": "To do List",
        "to_do_list": tool_context.state["to_do_list"],
    }


def complete_todo(task_number: int, tool_context: ToolContext) -> dict:
    """Mark a task as completed."""
    tmp_list = tool_context.state.get("to_do_list", [])

    if task_number < 1 or task_number > len(tmp_list):
        return {
            "statusMessage": "Invalid task number",
            "to_do_list": tool_context.state["to_do_list"],
        }

    tmp_list[task_number - 1]["done"] = True
    tool_context.state["to_do_list"] = tmp_list

    return {
        "statusMessage": f"Completed task {task_number}",
        "to_do_list": tool_context.state["to_do_list"],
    }


def delete_todo(task_number: int, tool_context: ToolContext) -> dict:
    """Delete a task from the todo list."""

    tmp_list = tool_context.state.get("to_do_list", [])

    if task_number < 1 or task_number > len(tmp_list):
        return {
            "statusMessage": "Invalid task number",
            "to_do_list": tool_context.state["to_do_list"],
        }

    removed = tmp_list.pop(task_number - 1)

    tool_context.state["to_do_list"] = tmp_list
    return {
        "statusMessage": f"Deleted task: {removed['task']}",
        "to_do_list": tool_context.state["to_do_list"],
    }


build_tools: list = [add_todo, list_todos, complete_todo, delete_todo]
