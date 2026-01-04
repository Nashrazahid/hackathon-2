"""
Todo service for the console todo application.

This module implements the service layer with in-memory task storage and operations.
"""

from typing import List, Optional, Dict
from src.models.task import Task


class TodoService:
    """
    Service layer for managing tasks with in-memory storage.

    This class handles all business logic related to tasks,
    including storage, retrieval, updates, and deletion.
    """

    def __init__(self):
        """Initialize the service with empty task collection."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task to the collection.

        Args:
            title (str): Task title
            description (str, optional): Task description

        Returns:
            Task: The created task with auto-generated ID

        Raises:
            ValueError: If title validation fails
        """
        # Validate inputs
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or contain only whitespace")

        if len(title.strip()) > 200:
            raise ValueError(f"Task title must be 200 characters or less, got {len(title.strip())}")

        if description is not None and (len(description.strip()) < 1 or len(description.strip()) > 1000):
            raise ValueError(f"Task description must be between 1 and 1000 characters, got {len(description.strip())}")

        # Create task with auto-generated ID
        task_id = self._next_id
        self._next_id += 1

        task = Task(task_id, title.strip(), description)
        self._tasks[task_id] = task

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Task or None: The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        """
        List all tasks in the collection.

        Returns:
            List[Task]: A list of all tasks
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title
            description (str, optional): New description

        Returns:
            Task or None: The updated task if found, None otherwise

        Raises:
            ValueError: If validation fails for new values
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]

        # Validate new title if provided
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty or contain only whitespace")

            if len(title.strip()) > 200:
                raise ValueError(f"Task title must be 200 characters or less, got {len(title.strip())}")

        # Validate new description if provided
        if description is not None and (len(description.strip()) < 1 or len(description.strip()) > 1000):
            raise ValueError(f"Task description must be between 1 and 1000 characters, got {len(description.strip())}")

        # Update task
        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description

        return task

    def mark_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            bool: True if task was found and updated, False otherwise
        """
        if task_id not in self._tasks:
            return False

        self._tasks[task_id].completed = True
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            bool: True if task was found and updated, False otherwise
        """
        if task_id not in self._tasks:
            return False

        self._tasks[task_id].completed = False
        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the collection.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if task was found and deleted, False otherwise
        """
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True

    def get_next_id(self) -> int:
        """
        Get the next available task ID.

        Returns:
            int: The next available task ID
        """
        return self._next_id

    def clear_all_tasks(self) -> None:
        """
        Clear all tasks from the collection (for testing purposes).
        """
        self._tasks.clear()
        self._next_id = 1