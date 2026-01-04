"""
Contract tests for CLI menu-driven interface in the todo application.

These tests verify that CLI menu-driven operations adhere to the specified contracts.
"""
import pytest
from io import StringIO
from unittest.mock import patch
from src.main import TodoCLI


class TestCLIMenuDrivenContract:
    """Test cases for basic CLI menu-driven operations."""

    def setup_method(self):
        """Set up a fresh CLI instance for each test."""
        self.cli = TodoCLI()
        # Clear any existing tasks for a clean test
        self.cli.controller.service.clear_all_tasks()

    def test_add_task_via_menu_contract(self):
        """Test ADD task via menu contract."""
        # Test successful add task via menu
        with patch('builtins.input', side_effect=['Test Title', 'Test Description']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_add_task_menu()
                output = mock_stdout.getvalue()
                assert "Task added successfully" in output
                assert "ID:" in output

        # Verify the task was actually created
        tasks = self.cli.controller.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Title"
        assert tasks[0].description == "Test Description"

    def test_add_task_without_description_via_menu_contract(self):
        """Test ADD task without description via menu."""
        with patch('builtins.input', side_effect=['Test Title', '']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_add_task_menu()
                output = mock_stdout.getvalue()
                assert "Task added successfully" in output

        tasks = self.cli.controller.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Title"
        assert tasks[0].description is None

    def test_list_tasks_via_menu_contract(self):
        """Test LIST tasks via menu contract."""
        # Add a task first
        self.cli.controller.add_task("Test Title", "Test Description")

        # Test list tasks via menu
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.handle_list_tasks()
            output = mock_stdout.getvalue()
            assert "Test Title" in output
            assert "Test Description" in output

    def test_update_task_via_menu_contract(self):
        """Test UPDATE task via menu contract."""
        # Add a task first
        task = self.cli.controller.add_task("Original Title", "Original Description")

        # Test update task via menu
        with patch('builtins.input', side_effect=[str(task.id), "New Title", "New Description"]):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_update_task_menu()
                output = mock_stdout.getvalue()
                assert f"Task {task.id} updated successfully" in output

        # Verify the task was updated
        updated_task = self.cli.controller.get_task(task.id)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_delete_task_via_menu_contract(self):
        """Test DELETE task via menu contract."""
        # Add a task first
        task = self.cli.controller.add_task("Test Title", "Test Description")

        # Test delete task via menu
        with patch('builtins.input', side_effect=[str(task.id)]):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_delete_task_menu()
                output = mock_stdout.getvalue()
                assert f"Task {task.id} deleted successfully" in output

        # Verify the task was deleted
        remaining_tasks = self.cli.controller.list_tasks()
        assert len(remaining_tasks) == 0

    def test_mark_complete_task_via_menu_contract(self):
        """Test MARK COMPLETE task via menu contract."""
        # Add a task first
        task = self.cli.controller.add_task("Test Title", "Test Description")
        assert task.completed is False

        # Test mark complete via menu
        with patch('builtins.input', side_effect=[str(task.id)]):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_mark_complete_menu()
                output = mock_stdout.getvalue()
                assert f"Task {task.id} marked as complete" in output

        # Verify the task was marked complete
        completed_task = self.cli.controller.get_task(task.id)
        assert completed_task.completed is True

    def test_exit_via_menu_contract(self):
        """Test EXIT via menu contract."""
        # Test exit via menu
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.handle_exit()
            output = mock_stdout.getvalue()
            assert "Goodbye! Your tasks are gone forever" in output

        assert self.cli.running is False


class TestCLIMenuDrivenErrorHandlingContract:
    """Test cases for CLI menu-driven error handling contracts."""

    def setup_method(self):
        """Set up a fresh CLI instance for each test."""
        self.cli = TodoCLI()
        # Clear any existing tasks for a clean test
        self.cli.controller.service.clear_all_tasks()

    def test_add_task_error_handling_via_menu(self):
        """Test ADD task error handling via menu."""
        # Test with empty title
        with patch('builtins.input', side_effect=['', 'Test Description']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_add_task_menu()
                output = mock_stdout.getvalue()
                assert "Error:" in output
                assert "cannot be empty" in output

    def test_update_task_error_handling_via_menu(self):
        """Test UPDATE task error handling via menu."""
        # Test updating non-existent task
        with patch('builtins.input', side_effect=['999', 'New Title', 'New Description']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_update_task_menu()
                output = mock_stdout.getvalue()
                assert "Error:" in output
                assert "not found" in output.lower()

        # Test with invalid ID
        with patch('builtins.input', side_effect=['invalid_id', 'New Title', 'New Description']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_update_task_menu()
                output = mock_stdout.getvalue()
                assert "Error:" in output
                assert "number" in output.lower()

    def test_delete_task_error_handling_via_menu(self):
        """Test DELETE task error handling via menu."""
        # Test deleting non-existent task
        with patch('builtins.input', side_effect=['999']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_delete_task_menu()
                output = mock_stdout.getvalue()
                assert "Error:" in output
                assert "not found" in output.lower()

        # Test with invalid ID
        with patch('builtins.input', side_effect=['invalid_id']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_delete_task_menu()
                output = mock_stdout.getvalue()
                assert "Error:" in output
                assert "number" in output.lower()

    def test_mark_complete_error_handling_via_menu(self):
        """Test MARK COMPLETE error handling via menu."""
        # Test marking non-existent task complete
        with patch('builtins.input', side_effect=['999']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_mark_complete_menu()
                output = mock_stdout.getvalue()
                assert "Error:" in output
                assert "not found" in output.lower()

        # Test with invalid ID
        with patch('builtins.input', side_effect=['invalid_id']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_mark_complete_menu()
                output = mock_stdout.getvalue()
                assert "Error:" in output
                assert "number" in output.lower()


class TestCLIMenuDrivenResponseFormatContract:
    """Test cases for CLI menu-driven response format contracts."""

    def setup_method(self):
        """Set up a fresh CLI instance for each test."""
        self.cli = TodoCLI()
        # Clear any existing tasks for a clean test
        self.cli.controller.service.clear_all_tasks()

    def test_add_task_success_response_format_via_menu(self):
        """Test ADD task success response format via menu."""
        with patch('builtins.input', side_effect=['Test Title', 'Test Description']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_add_task_menu()
                output = mock_stdout.getvalue().strip()
                # Should match: "Task added successfully with ID: {id}"
                assert "Task added successfully with ID:" in output

    def test_list_tasks_empty_response_format_via_menu(self):
        """Test LIST tasks empty response format via menu."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.handle_list_tasks()
            output = mock_stdout.getvalue().strip()
            assert "No tasks found." in output

    def test_delete_task_success_response_format_via_menu(self):
        """Test DELETE task success response format via menu."""
        task = self.cli.controller.add_task("Test Title", "Test Description")
        with patch('builtins.input', side_effect=[str(task.id)]):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_delete_task_menu()
                output = mock_stdout.getvalue().strip()
                # Should match: "Task {id} deleted successfully"
                assert f"Task {task.id} deleted successfully" in output

    def test_mark_complete_success_response_format_via_menu(self):
        """Test MARK COMPLETE success response format via menu."""
        task = self.cli.controller.add_task("Test Title", "Test Description")
        with patch('builtins.input', side_effect=[str(task.id)]):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.handle_mark_complete_menu()
                output = mock_stdout.getvalue().strip()
                # Should match: "Task {id} marked as complete"
                assert f"Task {task.id} marked as complete" in output

    def test_exit_success_response_format_via_menu(self):
        """Test EXIT success response format via menu."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.handle_exit()
            output = mock_stdout.getvalue()
            # Should match: "Goodbye! Your tasks are gone forever (in-memory only)."
            assert "Goodbye! Your tasks are gone forever (in-memory only)." in output