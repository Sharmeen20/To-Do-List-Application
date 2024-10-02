
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

# Function to view all tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks to show!")
    else:
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

# Function to edit a task
def edit_task(tasks):
    if not tasks:
        print("No tasks to edit!")
    else:
        view_tasks(tasks)
        try:
            task_num = int(input("Enter the task number to edit: "))
            if 0 < task_num <= len(tasks):
                new_task = input("Enter the new task: ")
                tasks[task_num - 1] = new_task
                save_tasks(tasks)
                print(f"Task {task_num} edited successfully!")
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
