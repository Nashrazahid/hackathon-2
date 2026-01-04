# Quickstart: Console Todo Application

**Created**: 2026-01-02
**Feature**: Console Todo Application
**Branch**: 001-console-todo-app

## Getting Started

### Prerequisites
- Python 3.13+ installed on your system
- Basic knowledge of command line interface

### Setup
1. Clone or download the project repository
2. Navigate to the project directory
3. Ensure Python 3.13+ is available in your environment

### Running the Application
```bash
python src/main.py
```

## Using the Application

### Main Menu
When you run the application, you'll see a menu with the following options:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

### Adding a Task
1. Select option 1 from the main menu
2. Enter the task title when prompted
3. Optionally enter a task description
4. The system will confirm the task was added with its ID

### Viewing Tasks
1. Select option 2 from the main menu
2. All tasks will be displayed with their ID, title, description, and completion status

### Updating a Task
1. Select option 3 from the main menu
2. Enter the task ID you want to update
3. Enter the new title and description when prompted
4. The system will confirm the update

### Deleting a Task
1. Select option 4 from the main menu
2. Enter the task ID you want to delete
3. The system will confirm the deletion

### Marking a Task Complete
1. Select option 5 from the main menu
2. Enter the task ID you want to mark as complete
3. The system will confirm the change

### Marking a Task Incomplete
1. Select option 6 from the main menu
2. Enter the task ID you want to mark as incomplete
3. The system will confirm the change

## Important Notes
- All data is stored in memory only and will be lost when the application closes
- Task IDs are automatically generated and unique within the session
- The application validates all inputs to prevent errors
- Use option 7 to exit the application properly