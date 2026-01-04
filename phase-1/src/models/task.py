"""
Task model for the console todo application.

This module defines the Task class with fields: id, title, description, and completed status.
It includes validation rules as specified in the data model.
"""

from typing import Optional


class Task:
    """
    Represents a single todo item with id, title, description, and completion status.

    Attributes:
        id (int): Unique identifier for the task
        title (str): Task title (required, max 200 characters)
        description (str): Task description (optional, max 1000 characters)
        completed (bool): Completion status (default: False)
    """

    def __init__(self, task_id: int, title: str, description: Optional[str] = None, completed: bool = False):
        """
        Initialize a Task instance with validation.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Task title (required, max 200 characters)
            description (str, optional): Task description (max 1000 characters)
            completed (bool): Completion status (default: False)

        Raises:
            ValueError: If validation rules are violated
        """
        self.id = self._validate_id(task_id)
        self.title = self._validate_title(title)
        self.description = self._validate_description(description)
        self.completed = completed

    def _validate_id(self, task_id: int) -> int:
        """Validate task ID."""
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError(f"Task ID must be a positive integer, got {task_id}")
        return task_id

    def _validate_title(self, title: str) -> str:
        """Validate task title."""
        if not isinstance(title, str):
            raise ValueError(f"Title must be a string, got {type(title).__name__}")

        if not title or not title.strip():
            raise ValueError("Title must not be empty or contain only whitespace")

        if len(title) > 200:
            raise ValueError(f"Title must be between 1 and 200 characters, got {len(title)}")

        return title.strip()

    def _validate_description(self, description: Optional[str]) -> Optional[str]:
        """Validate task description."""
        if description is None:
            return None

        if not isinstance(description, str):
            raise ValueError(f"Description must be a string or None, got {type(description).__name__}")

        # If description is provided but is just whitespace, we'll treat it as None
        if description and description.strip() == "":
            return None

        # If description has content, it must be between 1 and 1000 characters
        if description and (len(description.strip()) < 1 or len(description.strip()) > 1000):
            raise ValueError(f"Description must be between 1 and 1000 characters, got {len(description.strip())}")

        return description.strip() if description else None

    def update(self, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None):
        """
        Update task attributes with validation.

        Args:
            title (str, optional): New title
            description (str, optional): New description
            completed (bool, optional): New completion status
        """
        if title is not None:
            self.title = self._validate_title(title)
        if description is not None:
            self.description = self._validate_description(description)
        if completed is not None:
            if not isinstance(completed, bool):
                raise ValueError(f"Completed status must be a boolean, got {type(completed).__name__}")
            self.completed = completed

    def __repr__(self):
        """String representation of the Task."""
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"

    def __eq__(self, other):
        """Check equality based on all attributes."""
        if not isinstance(other, Task):
            return False
        return (self.id == other.id and
                self.title == other.title and
                self.description == other.description and
                self.completed == other.completed)

    def to_dict(self):
        """Convert task to dictionary representation."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }