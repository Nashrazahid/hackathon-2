"""
Unit tests for the TodoService.

These tests verify that the TodoService works correctly.
"""
import pytest
from src.services.todo_service import TodoService
from src.models.task import Task


class TestTodoService:
    """Test cases for the TodoService."""

    def setup_method(self):
        """Set up a fresh service instance for each test."""
        self.service = TodoService()

    def test_add_task_creates_task_with_correct_attributes(self):
        """Test adding a task with title and description."""
        task = self.service.add_task("Test Title", "Test Description")

        assert isinstance(task, Task)
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_add_task_without_description(self):
        """Test adding a task with only a title."""
        task = self.service.add_task("Test Title")

        assert isinstance(task, Task)
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description is None
        assert task.completed is False

    def test_add_task_generates_unique_ids(self):
        """Test that adding multiple tasks generates unique IDs."""
        task1 = self.service.add_task("Title 1")
        task2 = self.service.add_task("Title 2")
        task3 = self.service.add_task("Title 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_empty_title_raises_error(self):
        """Test that adding a task with empty title raises ValueError."""
        with pytest.raises(ValueError):
            self.service.add_task("")

        with pytest.raises(ValueError):
            self.service.add_task("   ")

    def test_add_task_with_long_title_raises_error(self):
        """Test that adding a task with title longer than 200 chars raises ValueError."""
        long_title = "A" * 201
        with pytest.raises(ValueError):
            self.service.add_task(long_title)

    def test_add_task_with_long_description_raises_error(self):
        """Test that adding a task with description longer than 1000 chars raises ValueError."""
        long_description = "A" * 1001
        with pytest.raises(ValueError):
            self.service.add_task("Valid Title", long_description)

    def test_get_task_returns_correct_task(self):
        """Test retrieving a task by ID."""
        task = self.service.add_task("Test Title")
        retrieved_task = self.service.get_task(task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title
        assert retrieved_task.description == task.description
        assert retrieved_task.completed == task.completed

    def test_get_task_returns_none_for_nonexistent_id(self):
        """Test that getting a non-existent task returns None."""
        result = self.service.get_task(999)
        assert result is None

    def test_list_tasks_returns_all_tasks(self):
        """Test listing all tasks."""
        task1 = self.service.add_task("Title 1")
        task2 = self.service.add_task("Title 2")
        task3 = self.service.add_task("Title 3")

        tasks = self.service.list_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_list_tasks_returns_empty_list_when_no_tasks(self):
        """Test that listing tasks returns empty list when no tasks exist."""
        tasks = self.service.list_tasks()
        assert len(tasks) == 0

    def test_update_task_updates_attributes(self):
        """Test updating a task's attributes."""
        original_task = self.service.add_task("Original Title", "Original Description")
        updated_task = self.service.update_task(original_task.id, "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed  # Should remain unchanged

    def test_update_task_partial_update(self):
        """Test updating only some attributes of a task."""
        original_task = self.service.add_task("Original Title", "Original Description")
        updated_task = self.service.update_task(original_task.id, title="New Title")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged

    def test_update_task_returns_none_for_nonexistent_id(self):
        """Test that updating a non-existent task returns None."""
        result = self.service.update_task(999, "New Title")
        assert result is None

    def test_update_task_with_invalid_title_raises_error(self):
        """Test that updating with invalid title raises ValueError."""
        task = self.service.add_task("Original Title")

        with pytest.raises(ValueError):
            self.service.update_task(task.id, "")  # Empty title

        with pytest.raises(ValueError):
            self.service.update_task(task.id, "A" * 201)  # Title too long

    def test_update_task_with_invalid_description_raises_error(self):
        """Test that updating with invalid description raises ValueError."""
        task = self.service.add_task("Original Title")

        with pytest.raises(ValueError):
            self.service.update_task(task.id, description="A" * 1001)  # Description too long

    def test_mark_complete_sets_task_to_completed(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Test Title")
        assert task.completed is False

        success = self.service.mark_complete(task.id)
        updated_task = self.service.get_task(task.id)

        assert success is True
        assert updated_task.completed is True

    def test_mark_complete_returns_false_for_nonexistent_task(self):
        """Test that marking a non-existent task complete returns False."""
        result = self.service.mark_complete(999)
        assert result is False

    def test_mark_incomplete_sets_task_to_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.service.add_task("Test Title")
        # First mark it complete
        self.service.mark_complete(task.id)
        assert task.completed is True

        success = self.service.mark_incomplete(task.id)
        updated_task = self.service.get_task(task.id)

        assert success is True
        assert updated_task.completed is False

    def test_mark_incomplete_returns_false_for_nonexistent_task(self):
        """Test that marking a non-existent task incomplete returns False."""
        result = self.service.mark_incomplete(999)
        assert result is False

    def test_delete_task_removes_task(self):
        """Test deleting a task."""
        task = self.service.add_task("Test Title")
        assert self.service.get_task(task.id) is not None

        success = self.service.delete_task(task.id)
        result = self.service.get_task(task.id)

        assert success is True
        assert result is None

    def test_delete_task_returns_false_for_nonexistent_task(self):
        """Test that deleting a non-existent task returns False."""
        result = self.service.delete_task(999)
        assert result is False

    def test_get_next_id_returns_correct_next_id(self):
        """Test that get_next_id returns the next available ID."""
        assert self.service.get_next_id() == 1

        self.service.add_task("Title 1")
        assert self.service.get_next_id() == 2

        self.service.add_task("Title 2")
        assert self.service.get_next_id() == 3

    def test_clear_all_tasks_clears_collection(self):
        """Test clearing all tasks."""
        self.service.add_task("Title 1")
        self.service.add_task("Title 2")
        assert len(self.service.list_tasks()) == 2

        self.service.clear_all_tasks()
        assert len(self.service.list_tasks()) == 0
        assert self.service.get_next_id() == 1  # Should reset to 1

    def test_list_tasks_returns_empty_list_when_no_tasks(self):
        """Test that list_tasks returns an empty list when no tasks exist."""
        tasks = self.service.list_tasks()
        assert len(tasks) == 0

    def test_list_tasks_returns_all_tasks(self):
        """Test that list_tasks returns all tasks in the collection."""
        # Add multiple tasks
        task1 = self.service.add_task("Task 1", "Description 1")
        task2 = self.service.add_task("Task 2", "Description 2")
        task3 = self.service.add_task("Task 3", "Description 3")

        tasks = self.service.list_tasks()

        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_list_tasks_returns_independent_tasks(self):
        """Test that listed tasks are independent of the internal storage."""
        original_task = self.service.add_task("Original Title", "Original Description")

        tasks = self.service.list_tasks()
        listed_task = tasks[0]

        # Modify the original task in the service
        self.service.update_task(original_task.id, "Updated Title")

        # The listed task should reflect the update
        updated_tasks = self.service.list_tasks()
        assert updated_tasks[0].title == "Updated Title"

    def test_update_task_updates_attributes(self):
        """Test updating a task's attributes."""
        original_task = self.service.add_task("Original Title", "Original Description")
        updated_task = self.service.update_task(original_task.id, "New Title", "New Description")

        assert updated_task is not None
        assert updated_task.id == original_task.id
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"
        assert updated_task.completed == original_task.completed  # Should remain unchanged

    def test_update_task_partial_update(self):
        """Test updating only some attributes of a task."""
        original_task = self.service.add_task("Original Title", "Original Description")
        updated_task = self.service.update_task(original_task.id, title="New Title")

        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged

    def test_update_task_returns_none_for_nonexistent_id(self):
        """Test that updating a non-existent task returns None."""
        result = self.service.update_task(999, "New Title")
        assert result is None

    def test_update_task_with_invalid_title_raises_error(self):
        """Test that updating with invalid title raises ValueError."""
        task = self.service.add_task("Original Title")

        with pytest.raises(ValueError):
            self.service.update_task(task.id, "")  # Empty title

        with pytest.raises(ValueError):
            self.service.update_task(task.id, "A" * 201)  # Title too long

    def test_update_task_with_invalid_description_raises_error(self):
        """Test that updating with invalid description raises ValueError."""
        task = self.service.add_task("Original Title")

        with pytest.raises(ValueError):
            self.service.update_task(task.id, description="A" * 1001)  # Description too long

    def test_mark_complete_sets_task_to_completed(self):
        """Test marking a task as complete."""
        task = self.service.add_task("Test Title")
        assert task.completed is False

        success = self.service.mark_complete(task.id)
        updated_task = self.service.get_task(task.id)

        assert success is True
        assert updated_task.completed is True

    def test_mark_complete_returns_false_for_nonexistent_task(self):
        """Test that marking a non-existent task complete returns False."""
        result = self.service.mark_complete(999)
        assert result is False

    def test_mark_incomplete_sets_task_to_incomplete(self):
        """Test marking a task as incomplete."""
        task = self.service.add_task("Test Title")
        # First mark it complete
        self.service.mark_complete(task.id)
        assert task.completed is True

        success = self.service.mark_incomplete(task.id)
        updated_task = self.service.get_task(task.id)

        assert success is True
        assert updated_task.completed is False

    def test_mark_incomplete_returns_false_for_nonexistent_task(self):
        """Test that marking a non-existent task incomplete returns False."""
        result = self.service.mark_incomplete(999)
        assert result is False
    def test_delete_task_removes_task(self):
        """Test deleting a task."""
        task = self.service.add_task("Test Title")
        assert self.service.get_task(task.id) is not None

        success = self.service.delete_task(task.id)
        result = self.service.get_task(task.id)

        assert success is True
        assert result is None

    def test_delete_task_returns_false_for_nonexistent_task(self):
        """Test that deleting a non-existent task returns False."""
        result = self.service.delete_task(999)
        assert result is False
