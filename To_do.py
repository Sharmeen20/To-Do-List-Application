<<<<<<< HEAD
=======
from datetime import datetime
>>>>>>> a8a6ca691a92d9feafa8b81f458b3b0c121bc756
import os

# Function to display the menu
def display_menu():
    print("\n---- To-Do List ----")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Remove Task")
    print("4. Edit Task")
    print("5. Exit")

# Function to add a task
def add_task(tasks):
    task = input("Enter the task: ")
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{task}' added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks to show!")
            return

        sort_by = input("Sort by (date/priority/none) [none]: ").lower() or "none"
        if sort_by == "date":
            self.tasks.sort(key=lambda x: (x.due_date is None, x.due_date))
        elif sort_by == "priority":
            priority_order = {"High": 0, "Medium": 1, "Low": 2}
            self.tasks.sort(key=lambda x: priority_order[x.priority])

        print("\nYour Tasks:")
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")

# Function to remove a task
def remove_task(tasks):
    if not tasks:
        print("No tasks to remove!")
    else:
        view_tasks(tasks)
        try:
            task_num = int(input("Enter the task number to remove: "))
            if 0 < task_num <= len(tasks):
                removed_task = tasks.pop(task_num - 1)
                save_tasks(tasks)
                print(f"Task '{removed_task}' removed successfully!")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

    def mark_completed(self):
        if not self.tasks:
            print("No tasks to mark as completed!")
            return

        self.view_tasks()
        try:
<<<<<<< HEAD
            task_num = int(input("Enter the task number to mark as completed: "))
            if 0 < task_num <= len(self.tasks):
                task = self.tasks[task_num - 1]
                task.completed = True
                self.save_tasks()
                print(f"Task '{task.description}' marked as completed!")
=======
            task_num = int(input("Enter the task number to edit: "))
            if 0 < task_num <= len(tasks):
                # Get current task details
                current_task = tasks[task_num - 1]
                
                # Edit task description
                new_task = input(f"Enter the new task (leave blank to keep '{current_task['task']}'): ")
                if new_task:
                    current_task['task'] = new_task

                # Edit task deadline
                new_deadline = input(f"Enter new deadline (dd-mm-yyyy) or press Enter to keep current deadline ({current_task['deadline']}): ")
                if new_deadline:
                    try:
                        current_task['deadline'] = datetime.strptime(new_deadline, "%d-%m-%Y").date()
                    except ValueError:
                        print("Invalid date format! Deadline unchanged.")
                save_tasks(tasks)
                print(f"Task {task_num} edited successfully!")
>>>>>>> a8a6ca691a92d9feafa8b81f458b3b0c121bc756
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

# Function to save tasks to a file
def save_tasks(tasks):
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

# Function to load tasks from a file
def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            tasks = [line.strip() for line in file.readlines()]
        return tasks
    return []

# Main function
def main():
    tasks = load_tasks()
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            edit_task(tasks)
        elif choice == '5':
            print("Exiting To-Do List. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()