#!/usr/bin/env python3
"""
Main entry point for the console todo application.

This module implements the CLI loop and menu options following the contracts.
"""

import sys
from typing import Optional
from src.controllers.todo_controller import TodoController
from src.utils.validation import parse_task_args, format_tasks_list, clean_input


class TodoCLI:
    """
    Command Line Interface for the todo application.
    """

    def __init__(self):
        """Initialize the CLI with a TodoController instance."""
        self.controller = TodoController()
        self.running = True

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("           TODO APPLICATION")
        print("="*50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Exit")
        print("-"*50)


    def handle_list_tasks(self):
        """Handle listing all tasks."""
        try:
            tasks = self.controller.list_tasks()
            if not tasks:
                print("No tasks found.")
            else:
                print("\nYour Tasks:")
                print(format_tasks_list(tasks))
        except Exception as e:
            print(f"Error listing tasks: {e}")






    def handle_exit(self):
        """Handle exiting the application."""
        print("Goodbye! Your tasks are gone forever (in-memory only).")
        self.running = False

    def process_menu_choice(self, choice: str):
        """Process a user's menu choice."""
        try:
            option = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number between 1-6.")
            return

        if option == 1:
            self.handle_add_task_menu()
        elif option == 2:
            self.handle_list_tasks()
        elif option == 3:
            self.handle_update_task_menu()
        elif option == 4:
            self.handle_delete_task_menu()
        elif option == 5:
            self.handle_mark_complete_menu()
        elif option == 6:
            self.handle_exit()
        else:
            print("Invalid option. Please enter a number between 1-6.")

    def handle_add_task_menu(self):
        """Handle adding a new task via menu."""
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Task title cannot be empty.")
                return

            description = input("Enter task description (optional): ").strip()
            description = description if description else None

            task = self.controller.add_task(title, description)
            print(f"Task added successfully with ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def handle_update_task_menu(self):
        """Handle updating a task via menu."""
        try:
            task_id_input = input("Enter task ID to update: ").strip()
            try:
                task_id = int(task_id_input)
            except ValueError:
                print("Error: Task ID must be a number.")
                return

            # Check if task exists first
            existing_task = self.controller.get_task(task_id)
            if not existing_task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            new_title = input(f"Enter new title (current: '{existing_task.title}'): ").strip()
            if not new_title:
                new_title = existing_task.title  # Keep existing title if empty

            new_description = input(f"Enter new description (current: '{existing_task.description or 'None'}'): ").strip()
            if new_description == "":
                new_description = existing_task.description  # Keep existing description if empty input

            updated_task = self.controller.update_task(task_id, new_title, new_description)
            if updated_task:
                print(f"Task {task_id} updated successfully")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def handle_delete_task_menu(self):
        """Handle deleting a task via menu."""
        try:
            task_id_input = input("Enter task ID to delete: ").strip()
            try:
                task_id = int(task_id_input)
            except ValueError:
                print("Error: Task ID must be a number.")
                return

            success = self.controller.delete_task(task_id)
            if success:
                print(f"Task {task_id} deleted successfully")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def handle_mark_complete_menu(self):
        """Handle marking a task as complete via menu."""
        try:
            task_id_input = input("Enter task ID to mark complete: ").strip()
            try:
                task_id = int(task_id_input)
            except ValueError:
                print("Error: Task ID must be a number.")
                return

            success = self.controller.mark_complete(task_id)
            if success:
                print(f"Task {task_id} marked as complete")
            else:
                print(f"Error: Task with ID {task_id} not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run(self):
        """Run the main CLI loop."""
        print("Welcome to the Console Todo Application!")

        while self.running:
            try:
                self.display_menu()
                choice = input("Select an option (1-6): ").strip()
                self.process_menu_choice(choice)
            except KeyboardInterrupt:
                print("\n\nReceived interrupt signal. Exiting...")
                self.handle_exit()
            except EOFError:
                print("\n\nEnd of input. Exiting...")
                self.handle_exit()


def main():
    """Main function to run the application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()