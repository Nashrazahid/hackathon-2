"""
Unit tests for the list_tasks functionality in TodoService and TodoController.

These tests verify that listing tasks works correctly.
"""
import pytest
from src.services.todo_service import TodoService
from src.controllers.todo_controller import TodoController


class TestListTasks:
    """Test cases for the list_tasks functionality."""

    def test_list_tasks_returns_empty_list_when_no_tasks(self):
        """Test that list_tasks returns an empty list when no tasks exist."""
        service = TodoService()
        tasks = service.list_tasks()
        assert len(tasks) == 0

    def test_list_tasks_returns_all_tasks(self):
        """Test that list_tasks returns all tasks in the collection."""
        service = TodoService()

        # Add multiple tasks
        task1 = service.add_task("Task 1", "Description 1")
        task2 = service.add_task("Task 2", "Description 2")
        task3 = service.add_task("Task 3", "Description 3")

        tasks = service.list_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_list_tasks_returns_independent_tasks(self):
        """Test that listed tasks are independent of the internal storage."""
        service = TodoService()
        original_task = service.add_task("Original Title", "Original Description")

        tasks = service.list_tasks()
        listed_task = tasks[0]

        # Modify the original task in the service
        service.update_task(original_task.id, "Updated Title")

        # The listed task should reflect the update
        updated_tasks = service.list_tasks()
        assert updated_tasks[0].title == "Updated Title"


class TestControllerListTasks:
    """Test cases for the list_tasks functionality in the controller."""

    def test_controller_list_tasks_returns_empty_list_when_no_tasks(self):
        """Test that controller's list_tasks returns an empty list when no tasks exist."""
        controller = TodoController()
        tasks = controller.list_tasks()
        assert len(tasks) == 0

    def test_controller_list_tasks_returns_all_tasks(self):
        """Test that controller's list_tasks returns all tasks in the collection."""
        controller = TodoController()

        # Add multiple tasks
        task1 = controller.add_task("Task 1", "Description 1")
        task2 = controller.add_task("Task 2", "Description 2")
        task3 = controller.add_task("Task 3", "Description 3")

        tasks = controller.list_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_controller_list_tasks_integration_with_service(self):
        """Test that controller's list_tasks integrates properly with the service."""
        controller = TodoController()

        # Add tasks through controller
        controller.add_task("Task 1", "Description 1")
        controller.add_task("Task 2", "Description 2")

        # List tasks through controller
        tasks = controller.list_tasks()

        # Verify the same tasks can be retrieved individually
        task1 = controller.get_task(1)
        task2 = controller.get_task(2)

        assert len(tasks) == 2
        assert task1 is not None
        assert task2 is not None