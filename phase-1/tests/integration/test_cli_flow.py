"""
Integration tests for CLI flows in the todo application.

These tests verify that the CLI flows work correctly from end to end.
"""
import pytest
from io import StringIO
from unittest.mock import patch
from src.main import TodoCLI


class TestCLIFlows:
    """Test cases for CLI integration flows."""

    def setup_method(self):
        """Set up a fresh CLI instance for each test."""
        self.cli = TodoCLI()
        # Clear any existing tasks for a clean test
        self.cli.controller.service.clear_all_tasks()

    def test_add_and_list_tasks_flow(self):
        """Test the flow of adding tasks and then listing them."""
        # Add a task
        self.cli.controller.add_task("Test Task 1", "Description for task 1")
        self.cli.controller.add_task("Test Task 2", "Description for task 2")

        # List tasks
        tasks = self.cli.controller.list_tasks()

        # Verify both tasks exist
        assert len(tasks) == 2
        titles = [task.title for task in tasks]
        assert "Test Task 1" in titles
        assert "Test Task 2" in titles

    def test_add_update_and_view_task_flow(self):
        """Test the flow of adding a task, updating it, and viewing it."""
        # Add a task
        task = self.cli.controller.add_task("Original Title", "Original Description")
        original_id = task.id

        # Update the task
        updated_task = self.cli.controller.update_task(
            original_id, "Updated Title", "Updated Description"
        )

        # Verify the update
        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"

        # Retrieve the task directly to verify persistence
        retrieved_task = self.cli.controller.get_task(original_id)
        assert retrieved_task.title == "Updated Title"
        assert retrieved_task.description == "Updated Description"

    def test_add_mark_complete_and_view_flow(self):
        """Test the flow of adding a task, marking it complete, and viewing it."""
        # Add a task
        task = self.cli.controller.add_task("Test Task", "Description")
        task_id = task.id

        # Verify it's initially incomplete
        assert task.completed is False

        # Mark it complete
        success = self.cli.controller.mark_complete(task_id)
        assert success is True

        # Verify it's now complete
        updated_task = self.cli.controller.get_task(task_id)
        assert updated_task.completed is True

    def test_add_delete_flow(self):
        """Test the flow of adding a task and then deleting it."""
        # Add a task
        task = self.cli.controller.add_task("Task to Delete", "Description")
        task_id = task.id

        # Verify it exists
        assert self.cli.controller.get_task(task_id) is not None

        # Delete the task
        success = self.cli.controller.delete_task(task_id)
        assert success is True

        # Verify it no longer exists
        # After deletion, get_task should return None for the deleted task
        from src.services.todo_service import TodoService
        service_task = self.cli.controller.service.get_task(task_id)
        assert service_task is None

    def test_multiple_operations_on_same_task_flow(self):
        """Test multiple operations on the same task."""
        # Add a task
        task = self.cli.controller.add_task("Initial Title", "Initial Description")
        task_id = task.id

        # Update it
        self.cli.controller.update_task(task_id, "Updated Title")

        # Mark it complete
        self.cli.controller.mark_complete(task_id)

        # Verify final state
        final_task = self.cli.controller.get_task(task_id)
        assert final_task.title == "Updated Title"
        assert final_task.description == "Initial Description"  # Not updated
        assert final_task.completed is True

    def test_task_count_consistency_flow(self):
        """Test that task counts are consistent across operations."""
        # Initially no tasks
        assert self.cli.controller.get_task_count() == 0
        assert self.cli.controller.get_completed_task_count() == 0
        assert self.cli.controller.get_pending_task_count() == 0

        # Add a task
        self.cli.controller.add_task("Task 1", "Description 1")
        assert self.cli.controller.get_task_count() == 1
        assert self.cli.controller.get_completed_task_count() == 0
        assert self.cli.controller.get_pending_task_count() == 1

        # Add another task
        task2 = self.cli.controller.add_task("Task 2", "Description 2")
        assert self.cli.controller.get_task_count() == 2
        assert self.cli.controller.get_completed_task_count() == 0
        assert self.cli.controller.get_pending_task_count() == 2

        # Complete one task
        self.cli.controller.mark_complete(task2.id)
        assert self.cli.controller.get_task_count() == 2
        assert self.cli.controller.get_completed_task_count() == 1
        assert self.cli.controller.get_pending_task_count() == 1

        # Delete one task
        self.cli.controller.delete_task(task2.id)
        assert self.cli.controller.get_task_count() == 1
        assert self.cli.controller.get_completed_task_count() == 0  # The completed task was deleted
        assert self.cli.controller.get_pending_task_count() == 1


class TestMenuDrivenIntegration:
    """Test cases for menu-driven integration."""

    def setup_method(self):
        """Set up a fresh CLI instance for each test."""
        self.cli = TodoCLI()
        # Clear any existing tasks for a clean test
        self.cli.controller.service.clear_all_tasks()

    @patch('builtins.input', side_effect=['Test Title', 'Test Description'])
    def test_add_task_interactive_mode(self, mock_input):
        """Test adding a task in interactive mode."""
        # Test the handle_add_task_menu method
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.handle_add_task_menu()
            # Check that a task was created
            tasks = self.cli.controller.list_tasks()
            assert len(tasks) == 1
            assert tasks[0].title == "Test Title"
            assert tasks[0].description == "Test Description"

    def test_menu_driven_flow(self):
        """Test the flow of menu-driven operations."""
        # Add a task via menu
        with patch('builtins.input', side_effect=['Test Title', 'Test Description']):
            with patch('sys.stdout', new_callable=StringIO):
                self.cli.handle_add_task_menu()

        # List tasks
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.handle_list_tasks()
            output = mock_stdout.getvalue()
            assert 'Test Title' in output

        # Update the task via menu
        # First, get the task ID by listing
        tasks = self.cli.controller.list_tasks()
        assert len(tasks) == 1
        task_id = tasks[0].id

        with patch('builtins.input', side_effect=[str(task_id), 'Updated Title', 'Updated Description']):
            with patch('sys.stdout', new_callable=StringIO):
                self.cli.handle_update_task_menu()

        # Verify the update
        tasks = self.cli.controller.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Updated Title"

        # Mark task complete via menu
        with patch('builtins.input', side_effect=[str(task_id)]):
            with patch('sys.stdout', new_callable=StringIO):
                self.cli.handle_mark_complete_menu()

        # Verify completion
        tasks = self.cli.controller.list_tasks()
        assert tasks[0].completed is True