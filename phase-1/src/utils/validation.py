"""
Validation utilities for the console todo application.

This module contains input validation helpers and console formatting helpers.
"""

from typing import Any, Optional
import re


def validate_task_title(title: str) -> bool:
    """
    Validate a task title based on requirements.

    Args:
        title (str): The title to validate

    Returns:
        bool: True if title is valid, False otherwise
    """
    if not isinstance(title, str):
        return False

    if not title or not title.strip():
        return False

    if len(title.strip()) > 200:
        return False

    return True


def validate_task_description(description: Optional[str]) -> bool:
    """
    Validate a task description based on requirements.

    Args:
        description (str, optional): The description to validate

    Returns:
        bool: True if description is valid, False otherwise
    """
    if description is None:
        return True

    if not isinstance(description, str):
        return False

    # If it's a whitespace-only string, treat as None which is valid
    if description and description.strip() == "":
        return True

    # If it has content, it must be between 1 and 1000 characters
    if description and (len(description.strip()) < 1 or len(description.strip()) > 1000):
        return False

    return True


def validate_task_id(task_id: Any) -> bool:
    """
    Validate a task ID based on requirements.

    Args:
        task_id (Any): The ID to validate

    Returns:
        bool: True if ID is valid, False otherwise
    """
    if not isinstance(task_id, int):
        return False

    if task_id <= 0:
        return False

    return True


def validate_task_completion_status(completed: Any) -> bool:
    """
    Validate a task completion status based on requirements.

    Args:
        completed (Any): The completion status to validate

    Returns:
        bool: True if completion status is valid, False otherwise
    """
    return isinstance(completed, bool)


def format_task_display(task) -> str:
    """
    Format a task for display in the console.

    Args:
        task: A Task object to format

    Returns:
        str: Formatted string representation of the task
    """
    status = "✓" if task.completed else "○"
    description = task.description if task.description else "No description"
    return f"[{status}] ID: {task.id} | Title: {task.title} | Description: {description}"


def format_tasks_list(tasks) -> str:
    """
    Format a list of tasks for display in the console.

    Args:
        tasks: A list or collection of Task objects

    Returns:
        str: Formatted string representation of the tasks list
    """
    if not tasks:
        return "No tasks found."

    task_list = []
    for task in tasks:
        task_list.append(format_task_display(task))

    return "\n".join(task_list)


def is_valid_command(command: str, valid_commands: list) -> bool:
    """
    Check if a command is valid.

    Args:
        command (str): The command to validate
        valid_commands (list): List of valid commands

    Returns:
        bool: True if command is valid, False otherwise
    """
    if not isinstance(command, str):
        return False

    return command.lower() in [cmd.lower() for cmd in valid_commands]


def clean_input(user_input: str) -> str:
    """
    Clean user input by stripping whitespace.

    Args:
        user_input (str): The raw user input

    Returns:
        str: Cleaned user input
    """
    if not isinstance(user_input, str):
        return ""
    return user_input.strip()


def parse_task_args(args_str: str) -> tuple:
    """
    Parse task arguments from a string input.
    This function handles quoted strings as single arguments.

    Args:
        args_str (str): The arguments string

    Returns:
        tuple: Parsed arguments as a tuple
    """
    if not args_str.strip():
        return tuple()

    # This regex finds quoted strings or non-whitespace sequences
    pattern = r'"([^"]*)"|\'([^\']*)\'|(\S+)'
    matches = re.findall(pattern, args_str)

    # Each match is a tuple of (double_quoted, single_quoted, unquoted)
    args = []
    for match in matches:
        # The matched part will be in one of the three groups
        arg = next((m for m in match if m), '')
        args.append(arg)

    return tuple(args)