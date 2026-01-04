# CLI Contracts: Console Todo Application

**Created**: 2026-01-02
**Feature**: Console Todo Application
**Branch**: 001-console-todo-app

## Contract: CLI Interface

### Command: ADD_TASK
- **Input**: `add` command with title and optional description
- **Format**: `add "Task Title" "Optional Description"`
- **Success Response**: "Task added successfully with ID: {id}"
- **Error Response**: "Error: {error_message}"

### Command: LIST_TASKS
- **Input**: `list` or `view` command
- **Format**: `list`
- **Success Response**: Formatted list of all tasks with ID, title, description, and completion status
- **Error Response**: "No tasks found." (when no tasks exist)

### Command: UPDATE_TASK
- **Input**: `update` command with task ID and new information
- **Format**: `update {id} "New Title" "New Description"`
- **Success Response**: "Task {id} updated successfully"
- **Error Response**: "Error: {error_message}"

### Command: DELETE_TASK
- **Input**: `delete` command with task ID
- **Format**: `delete {id}`
- **Success Response**: "Task {id} deleted successfully"
- **Error Response**: "Error: {error_message}"

### Command: MARK_COMPLETE
- **Input**: `complete` command with task ID
- **Format**: `complete {id}`
- **Success Response**: "Task {id} marked as complete"
- **Error Response**: "Error: {error_message}"

### Command: MARK_INCOMPLETE
- **Input**: `incomplete` command with task ID
- **Format**: `incomplete {id}`
- **Success Response**: "Task {id} marked as incomplete"
- **Error Response**: "Error: {error_message}"

### Command: EXIT
- **Input**: `exit` or `quit` command
- **Format**: `exit`
- **Success Response**: "Goodbye! Your tasks are gone forever (in-memory only)."
- **Error Response**: N/A

### Command: HELP
- **Input**: `help` command
- **Format**: `help`
- **Success Response**: Display all available commands and their usage
- **Error Response**: N/A

## Validation Contracts

### Input Validation
- Task titles must be 1-200 characters
- Task descriptions must be 0-1000 characters
- Task IDs must be positive integers
- Invalid commands return appropriate error messages

### Error Handling Contract
- All errors return user-friendly messages
- Invalid inputs are handled gracefully
- Non-existent task IDs return appropriate error messages
- Application continues running after errors