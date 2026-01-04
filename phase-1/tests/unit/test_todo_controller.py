"""
Unit tests for the TodoController.

These tests verify that the TodoController handles validation correctly.
"""
import pytest
from src.controllers.todo_controller import TodoController
from src.models.task import Task


class TestTodoController:
    """Test cases for the TodoController."""

    def setup_method(self):
        """Set up a fresh controller instance for each test."""
        self.controller = TodoController()

    def test_add_task_creates_task_with_correct_attributes(self):
        """Test adding a task with title and description."""
        task = self.controller.add_task("Test Title", "Test Description")

        assert isinstance(task, Task)
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_add_task_without_description(self):
        """Test adding a task with only a title."""
        task = self.controller.add_task("Test Title")

        assert isinstance(task, Task)
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description is None
        assert task.completed is False

    def test_add_task_with_empty_title_raises_error(self):
        """Test that adding a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Invalid task title"):
            self.controller.add_task("")

        with pytest.raises(ValueError, match="Invalid task title"):
            self.controller.add_task("   ")

    def test_add_task_with_long_title_raises_error(self):
        """Test that adding a task with title longer than 200 chars raises ValueError."""
        long_title = "A" * 201
        with pytest.raises(ValueError, match="Invalid task title"):
            self.controller.add_task(long_title)

    def test_add_task_with_long_description_raises_error(self):
        """Test that adding a task with description longer than 1000 chars raises ValueError."""
        long_description = "A" * 1001
        with pytest.raises(ValueError, match="Invalid task description"):
            self.controller.add_task("Valid Title", long_description)

    def test_get_task_returns_correct_task(self):
        """Test retrieving a task by ID."""
        task = self.controller.add_task("Test Title")
        retrieved_task = self.controller.get_task(task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title
        assert retrieved_task.description == task.description
        assert retrieved_task.completed == task.completed

    def test_get_task_with_invalid_id_raises_error(self):
        """Test that getting a task with invalid ID raises ValueError."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.get_task(0)

        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.get_task(-1)

    def test_get_task_returns_none_for_nonexistent_id(self):
        """Test that getting a non-existent task returns None."""
        # Add a task to make sure there's at least one ID in the system
        self.controller.add_task("Test Title")

        # Try to get a task that doesn't exist
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.get_task(0)

    def test_list_tasks_returns_all_tasks(self):
        """Test listing all tasks."""
        task1 = self.controller.add_task("Title 1")
        task2 = self.controller.add_task("Title 2")
        task3 = self.controller.add_task("Title 3")

        tasks = self.controller.list_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_update_task_updates_attributes(self):
        """Test updating a task's attributes."""
        original_task = self.controller.add_task("Original Title", "Original Description")
        updated_task = self.controller.update_task(original_task.id, "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed  # Should remain unchanged

    def test_update_task_partial_update(self):
        """Test updating only some attributes of a task."""
        original_task = self.controller.add_task("Original Title", "Original Description")
        updated_task = self.controller.update_task(original_task.id, title="New Title")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged

    def test_update_task_with_invalid_id_raises_error(self):
        """Test that updating a task with invalid ID raises ValueError."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.update_task(0, "New Title")

        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.update_task(-1, "New Title")

    def test_update_task_with_invalid_title_raises_error(self):
        """Test that updating with invalid title raises ValueError."""
        task = self.controller.add_task("Original Title")

        with pytest.raises(ValueError, match="Invalid task title"):
            self.controller.update_task(task.id, "")  # Empty title

        with pytest.raises(ValueError, match="Invalid task title"):
            self.controller.update_task(task.id, "A" * 201)  # Title too long

    def test_update_task_with_invalid_description_raises_error(self):
        """Test that updating with invalid description raises ValueError."""
        task = self.controller.add_task("Original Title")

        with pytest.raises(ValueError, match="Invalid task description"):
            self.controller.update_task(task.id, description="A" * 1001)  # Description too long

    def test_mark_complete_sets_task_to_completed(self):
        """Test marking a task as complete."""
        task = self.controller.add_task("Test Title")
        assert task.completed is False

        success = self.controller.mark_complete(task.id)
        updated_task = self.controller.get_task(task.id)

        assert success is True
        assert updated_task.completed is True

    def test_mark_complete_with_invalid_id_raises_error(self):
        """Test that marking a task complete with invalid ID raises ValueError."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.mark_complete(0)

        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.mark_complete(-1)

    def test_mark_incomplete_sets_task_to_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.controller.add_task("Test Title")
        # First mark it complete
        self.controller.mark_complete(task.id)
        updated_task = self.controller.get_task(task.id)
        assert updated_task.completed is True

        success = self.controller.mark_incomplete(task.id)
        final_task = self.controller.get_task(task.id)

        assert success is True
        assert final_task.completed is False

    def test_mark_incomplete_with_invalid_id_raises_error(self):
        """Test that marking a task incomplete with invalid ID raises ValueError."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.mark_incomplete(0)

        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.mark_incomplete(-1)

    def test_delete_task_removes_task(self):
        """Test deleting a task."""
        task = self.controller.add_task("Test Title")
        assert self.controller.get_task(task.id) is not None

        success = self.controller.delete_task(task.id)
        # Getting the task after deletion should return None
        result = self.controller.get_task(task.id)
        assert result is None

        assert success is True

    def test_delete_task_with_invalid_id_raises_error(self):
        """Test that deleting a task with invalid ID raises ValueError."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.delete_task(0)

        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.delete_task(-1)

    def test_get_task_count(self):
        """Test getting the total task count."""
        assert self.controller.get_task_count() == 0

        self.controller.add_task("Title 1")
        assert self.controller.get_task_count() == 1

        self.controller.add_task("Title 2")
        assert self.controller.get_task_count() == 2

    def test_get_completed_task_count(self):
        """Test getting the completed task count."""
        # Add tasks, none completed
        self.controller.add_task("Task 1")
        self.controller.add_task("Task 2")
        assert self.controller.get_completed_task_count() == 0

        # Complete one task
        task = self.controller.add_task("Task 3")
        self.controller.mark_complete(task.id)
        assert self.controller.get_completed_task_count() == 1

        # Complete another task
        task2 = self.controller.add_task("Task 4")
        self.controller.mark_complete(task2.id)
        assert self.controller.get_completed_task_count() == 2

    def test_get_pending_task_count(self):
        """Test getting the pending task count."""
        # Add tasks, none completed
        self.controller.add_task("Task 1")
        self.controller.add_task("Task 2")
        assert self.controller.get_pending_task_count() == 2

        # Complete one task
        task = self.controller.add_task("Task 3")
        self.controller.mark_complete(task.id)
        assert self.controller.get_pending_task_count() == 2  # 2 pending, 1 completed

        # Complete another task
        task2 = self.controller.add_task("Task 4")
        self.controller.mark_complete(task2.id)
        assert self.controller.get_pending_task_count() == 2  # 2 pending, 2 completed

    def test_controller_list_tasks_returns_empty_list_when_no_tasks(self):
        """Test that controller's list_tasks returns an empty list when no tasks exist."""
        tasks = self.controller.list_tasks()
        assert len(tasks) == 0

    def test_controller_list_tasks_returns_all_tasks(self):
        """Test that controller's list_tasks returns all tasks in the collection."""
        # Add multiple tasks
        task1 = self.controller.add_task("Task 1", "Description 1")
        task2 = self.controller.add_task("Task 2", "Description 2")
        task3 = self.controller.add_task("Task 3", "Description 3")

        tasks = self.controller.list_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_controller_list_tasks_integration_with_service(self):
        """Test that controller's list_tasks integrates properly with the service."""
        # Add tasks through controller
        self.controller.add_task("Task 1", "Description 1")
        self.controller.add_task("Task 2", "Description 2")

        # List tasks through controller
        tasks = self.controller.list_tasks()

        # Verify the same tasks can be retrieved individually
        task1 = self.controller.get_task(1)
        task2 = self.controller.get_task(2)

        assert len(tasks) == 2
        assert task1 is not None
        assert task2 is not None

    def test_controller_update_task_updates_attributes(self):
        """Test updating a task's attributes via controller."""
        original_task = self.controller.add_task("Original Title", "Original Description")
        updated_task = self.controller.update_task(original_task.id, "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed  # Should remain unchanged

    def test_controller_update_task_partial_update(self):
        """Test updating only some attributes of a task via controller."""
        original_task = self.controller.add_task("Original Title", "Original Description")
        updated_task = self.controller.update_task(original_task.id, title="New Title")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged

    def test_controller_update_task_with_invalid_id_raises_error(self):
        """Test that updating a task with invalid ID raises ValueError via controller."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.update_task(0, "New Title")

        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.update_task(-1, "New Title")

    def test_controller_update_task_with_invalid_title_raises_error(self):
        """Test that updating with invalid title raises ValueError via controller."""
        task = self.controller.add_task("Original Title")

        with pytest.raises(ValueError, match="Invalid task title"):
            self.controller.update_task(task.id, "")  # Empty title

        with pytest.raises(ValueError, match="Invalid task title"):
            self.controller.update_task(task.id, "A" * 201)  # Title too long

    def test_controller_update_task_with_invalid_description_raises_error(self):
        """Test that updating with invalid description raises ValueError via controller."""
        task = self.controller.add_task("Original Title")

        with pytest.raises(ValueError, match="Invalid task description"):
            self.controller.update_task(task.id, description="A" * 1001)  # Description too long

    def test_controller_mark_complete_sets_task_to_completed(self):
        """Test marking a task as complete via controller."""
        task = self.controller.add_task("Test Title")
        assert task.completed is False

        success = self.controller.mark_complete(task.id)
        updated_task = self.controller.get_task(task.id)

        assert success is True
        assert updated_task.completed is True

    def test_controller_mark_complete_with_invalid_id_raises_error(self):
        """Test that marking a task complete with invalid ID raises ValueError via controller."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.mark_complete(0)

        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.mark_complete(-1)

    def test_controller_mark_incomplete_sets_task_to_incomplete(self):
        """Test marking a task as incomplete via controller."""
        task = self.controller.add_task("Test Title")
        # First mark it complete
        self.controller.mark_complete(task.id)
        updated_task = self.controller.get_task(task.id)
        assert updated_task.completed is True

        success = self.controller.mark_incomplete(task.id)
        final_task = self.controller.get_task(task.id)

        assert success is True
        assert final_task.completed is False

    def test_controller_mark_incomplete_with_invalid_id_raises_error(self):
        """Test that marking a task incomplete with invalid ID raises ValueError via controller."""
        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.mark_incomplete(0)

        with pytest.raises(ValueError, match="Invalid task ID"):
            self.controller.mark_incomplete(-1)