"""
Unit tests for the Task model.

These tests verify that the Task class works correctly according to the data model.
"""
import pytest
from src.models.task import Task


class TestTask:
    """Test cases for the Task model."""

    def test_create_task_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(1, "Test Title", "Test Description", False)
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_create_task_with_defaults(self):
        """Test creating a task with default values."""
        task = Task(1, "Test Title")
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description is None
        assert task.completed is False

    def test_create_task_auto_sets_completed_false(self):
        """Test that completed defaults to False."""
        task = Task(1, "Test Title")
        assert task.completed is False

    def test_invalid_id_raises_error(self):
        """Test that invalid ID raises ValueError."""
        with pytest.raises(ValueError):
            Task(0, "Test Title")  # ID must be positive

        with pytest.raises(ValueError):
            Task(-1, "Test Title")  # ID must be positive

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError):
            Task(1, "")  # Empty title

        with pytest.raises(ValueError):
            Task(1, "   ")  # Whitespace-only title

    def test_title_too_long_raises_error(self):
        """Test that title longer than 200 characters raises ValueError."""
        long_title = "A" * 201
        with pytest.raises(ValueError):
            Task(1, long_title)

    def test_description_too_long_raises_error(self):
        """Test that description longer than 1000 characters raises ValueError."""
        long_description = "A" * 1001
        with pytest.raises(ValueError):
            Task(1, "Valid Title", long_description)

    def test_title_gets_stripped(self):
        """Test that title whitespace is stripped."""
        task = Task(1, "  Title with spaces  ")
        assert task.title == "Title with spaces"

    def test_description_gets_stripped(self):
        """Test that description whitespace is stripped."""
        task = Task(1, "Title", "  Description with spaces  ")
        assert task.description == "Description with spaces"

    def test_whitespace_only_description_becomes_none(self):
        """Test that whitespace-only description becomes None."""
        task = Task(1, "Title", "   ")
        assert task.description is None

    def test_update_task_attributes(self):
        """Test updating task attributes."""
        task = Task(1, "Original Title", "Original Description", False)

        task.update(title="New Title", description="New Description", completed=True)
        assert task.title == "New Title"
        assert task.description == "New Description"
        assert task.completed is True

    def test_update_task_partial_attributes(self):
        """Test updating only some task attributes."""
        task = Task(1, "Original Title", "Original Description", False)

        task.update(title="New Title")
        assert task.title == "New Title"
        assert task.description == "Original Description"
        assert task.completed is False

    def test_update_task_invalid_completed_raises_error(self):
        """Test that updating with invalid completed value raises ValueError."""
        task = Task(1, "Title")

        with pytest.raises(ValueError):
            task.update(completed="invalid")

    def test_repr_returns_string_representation(self):
        """Test that __repr__ returns a string representation."""
        task = Task(1, "Test Title", "Test Description", True)
        repr_str = repr(task)
        assert "Task(id=1, title='Test Title', description='Test Description', completed=True)" in repr_str

    def test_to_dict_returns_correct_dict(self):
        """Test that to_dict returns correct dictionary representation."""
        task = Task(1, "Test Title", "Test Description", True)
        task_dict = task.to_dict()

        expected = {
            'id': 1,
            'title': 'Test Title',
            'description': 'Test Description',
            'completed': True
        }
        assert task_dict == expected