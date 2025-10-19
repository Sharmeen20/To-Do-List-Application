from datetime import datetime
import os

# Constants
TASKS_FILE = "tasks.txt"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n---- To-Do List ----"
          "\n1. Add Task"
          "\n2. View Tasks"
          "\n3. Mark Task as Completed"
          "\n4. Remove Task"
          "\n5. Edit Task"
          "\n6. Exit")

def add_task(tasks):
    task = input("Enter the task: ")
    deadline = input("Enter the deadline (dd-mm-yyyy) or press Enter to skip: ")
    priority = input("Enter priority (High / Medium / Low): ").capitalize()  # 👈 New priority input

    if deadline:
        try:
            deadline = datetime.strptime(deadline, "%d-%m-%Y").date()
        except ValueError:
            print("Invalid date format! Task added without deadline.")
            deadline = None
    else:
        deadline = None

    task_info = {
        'task': task,
        'completed': False,
        'deadline': deadline,
        'priority': priority if priority in ["High", "Medium", "Low"] else "Medium"  # 👈 Default to Medium
    }
    tasks.append(task_info)
    print(f"Task '{task}' added successfully!")

def view_tasks(tasks):
    if not tasks:
        print("No tasks to show!")
        return
    print("\nYour Tasks:")
    for idx, task_info in enumerate(tasks, 1):
        task_status = "[✔]" if task_info['completed'] else "[ ]"
        deadline = f"(Deadline: {task_info['deadline']})" if task_info['deadline'] else ""
        priority = f"[Priority: {task_info['priority']}]"  # 👈 Show priority
        print(f"{idx}. {task_status} {task_info['task']} {priority} {deadline}")

def mark_task_completed(tasks):
    if not tasks:
        print("No tasks to mark as completed!")
        return
    view_tasks(tasks)
    task_num = input("Enter the task number to mark as completed: ")
    if task_num.isdigit():
        task_num = int(task_num)
        if 0 < task_num <= len(tasks):
            tasks[task_num - 1]['completed'] = True
            print(f"Task '{tasks[task_num - 1]['task']}' marked as completed!")
        else:
            print("Invalid task number!")
    else:
        print("Please enter a valid number!")

def remove_task(tasks):
    if not tasks:
        print("No tasks to remove!")
        return
    view_tasks(tasks)
    try:
        task_num = int(input("Enter the task number to remove: "))
        if 0 < task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            print(f"Task '{removed_task['task']}' removed successfully!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def edit_task(tasks):
    if not tasks:
        print("No tasks to edit!")
        return
    view_tasks(tasks)
    try:
        task_num = int(input("Enter the task number to edit: "))
        if 0 < task_num <= len(tasks):
            current_task = tasks[task_num - 1]
            new_task = input(f"Enter the new task (leave blank to keep '{current_task['task']}'): ")
            if new_task:
                current_task['task'] = new_task

            new_deadline = input(f"Enter new deadline (dd-mm-yyyy) or press Enter to keep current deadline ({current_task['deadline'] or 'None'}): ")
            if new_deadline:
                try:
                    current_task['deadline'] = datetime.strptime(new_deadline, "%d-%m-%Y").date()
                except ValueError:
                    print("Invalid date format! Deadline unchanged.")

            new_priority = input(f"Enter new priority (High / Medium / Low) or press Enter to keep current ({current_task['priority']}): ").capitalize()
            if new_priority in ["High", "Medium", "Low"]:
                current_task['priority'] = new_priority

            print(f"Task {task_num} edited successfully!")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        for task_info in tasks:
            task = task_info['task']
            completed = str(task_info['completed'])
            deadline = task_info['deadline'].strftime('%d-%m-%Y') if task_info['deadline'] else "None"
            priority = task_info['priority']
            file.write(f"{task},{completed},{deadline},{priority}\n")  # 👈 Save priority

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = []
            for line in file:
                parts = line.strip().split(',')
                task = parts[0]
                completed = parts[1] == 'True'
                deadline = datetime.strptime(parts[2], '%d-%m-%Y').date() if parts[2] != "None" else None
                priority = parts[3] if len(parts) > 3 else "Medium"
                tasks.append({'task': task, 'completed': completed, 'deadline': deadline, 'priority': priority})
            return tasks
    return []

def main():
    tasks = load_tasks()
    menu_options = {
        "1": add_task,
        "2": view_tasks,
        "3": mark_task_completed,
        "4": remove_task,
        "5": edit_task,
        "6": lambda tasks: [print("Saving tasks and exiting To-Do List. Goodbye!"), save_tasks(tasks), exit()]
    }

    while True:
        clear_screen()
        display_menu()
        choice = input("Enter your choice: ")
        if choice in menu_options:
            menu_optionschoice
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
