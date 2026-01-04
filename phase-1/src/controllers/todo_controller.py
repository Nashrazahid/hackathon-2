"""
Todo controller for the console todo application.

This module handles input validation and business logic coordination.
"""

from typing import List, Optional
from src.services.todo_service import TodoService
from src.models.task import Task
from src.utils.validation import validate_task_title, validate_task_description, validate_task_id


class TodoController:
    """
    Controller layer for handling user input validation and coordinating with service layer.
    """

    def __init__(self):
        """Initialize the controller with a TodoService instance."""
        self.service = TodoService()

    def add_task(self, title: str, description: Optional[str] = None) -> Optional[Task]:
        """
        Add a new task after validating inputs.

        Args:
            title (str): Task title
            description (str, optional): Task description

        Returns:
            Task or None: The created task if successful, None otherwise

        Raises:
            ValueError: If input validation fails
        """
        # Validate inputs
        if not validate_task_title(title):
            raise ValueError("Invalid task title. Title must be 1-200 characters and not empty.")

        if description is not None and not validate_task_description(description):
            raise ValueError("Invalid task description. Description must be 1-1000 characters.")

        # Call service to add task
        return self.service.add_task(title, description)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID after validating the ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task if found, None otherwise
        """
        if not validate_task_id(task_id):
            raise ValueError(f"Invalid task ID: {task_id}. Task ID must be a positive integer.")

        return self.service.get_task(task_id)

    def list_tasks(self) -> List[Task]:
        """
        List all tasks.

        Returns:
            List[Task]: A list of all tasks
        """
        return self.service.list_tasks()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task after validating inputs.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title
            description (str, optional): New description

        Returns:
            Task or None: The updated task if found, None otherwise

        Raises:
            ValueError: If input validation fails
        """
        if not validate_task_id(task_id):
            raise ValueError(f"Invalid task ID: {task_id}. Task ID must be a positive integer.")

        if title is not None and not validate_task_title(title):
            raise ValueError("Invalid task title. Title must be 1-200 characters and not empty.")

        if description is not None and not validate_task_description(description):
            raise ValueError("Invalid task description. Description must be 1-1000 characters.")

        return self.service.update_task(task_id, title, description)

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete after validating the ID.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            bool: True if task was found and updated, False otherwise
        """
        if not validate_task_id(task_id):
            raise ValueError(f"Invalid task ID: {task_id}. Task ID must be a positive integer.")

        return self.service.mark_complete(task_id)

    def mark_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete after validating the ID.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            bool: True if task was found and updated, False otherwise
        """
        if not validate_task_id(task_id):
            raise ValueError(f"Invalid task ID: {task_id}. Task ID must be a positive integer.")

        return self.service.mark_incomplete(task_id)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task after validating the ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if task was found and deleted, False otherwise
        """
        if not validate_task_id(task_id):
            raise ValueError(f"Invalid task ID: {task_id}. Task ID must be a positive integer.")

        return self.service.delete_task(task_id)

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            int: The number of tasks in the collection
        """
        return len(self.service.list_tasks())

    def get_completed_task_count(self) -> int:
        """
        Get the number of completed tasks.

        Returns:
            int: The number of completed tasks
        """
        tasks = self.service.list_tasks()
        return sum(1 for task in tasks if task.completed)

    def get_pending_task_count(self) -> int:
        """
        Get the number of pending (not completed) tasks.

        Returns:
            int: The number of pending tasks
        """
        tasks = self.service.list_tasks()
        return sum(1 for task in tasks if not task.completed)