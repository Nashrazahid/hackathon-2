# Data Model: Console Todo Application

**Created**: 2026-01-02
**Feature**: Console Todo Application
**Branch**: 001-console-todo-app

## Entity: Task

### Fields
- **id**: Integer (Unique identifier, auto-generated)
- **title**: String (Required, max 200 characters)
- **description**: String (Optional, max 1000 characters)
- **completed**: Boolean (Default: False)

### Validation Rules
- Title must not be empty or contain only whitespace
- Title must be between 1 and 200 characters
- Description, if provided, must be between 1 and 1000 characters
- ID must be unique within the application session

### State Transitions
- New Task: `completed = False` (default)
- Updated Task: `completed` can change from `False` to `True` or `True` to `False`
- Deleted Task: Task is removed from the collection

### Relationships
- No relationships with other entities (standalone entity)

## Entity: TaskCollection (In-Memory Storage)

### Fields
- **tasks**: Dictionary (Key: task_id, Value: Task object)
- **next_id**: Integer (Auto-incrementing ID counter)

### Operations
- Add Task: Insert a new task with auto-generated ID
- Get Task: Retrieve task by ID
- Update Task: Modify existing task by ID
- Delete Task: Remove task by ID
- List Tasks: Return all tasks in the collection

### Validation Rules
- Task IDs must be unique
- No duplicate IDs allowed
- Task objects must be valid according to Task entity rules