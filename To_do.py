from datetime import datetime
import os
# Constants
TASKS_FILE = "tasks.txt"
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def display_menu():
    print("\n---- To-Do List ----""\n1. Add Task""\n2. View Tasks""\n3. Mark Task as Completed""\n4. Remove Task""\n5. Edit Task""\n6. Exit")
def add_task(tasks):
    task = input("Enter the task: ")
    deadline = input("Enter the deadline (dd-mm-yyyy) or press Enter to skip: ")
    if deadline:
        try:
            deadline = datetime.strptime(deadline, "%d-%m-%Y").date()
        except ValueError:
            print("Invalid date format! Task added without deadline.")
            deadline = None
    else:
        deadline = None
    task_info = {'task': task, 'completed': False, 'deadline': deadline}
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
        print(f"{idx}. {task_status} {task_info['task']} {deadline}")
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
            file.write(f"{task},{completed},{deadline}\n")
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = []
            for line in file:
                task, completed, deadline = line.strip().split(',')
                completed = completed == 'True'
                deadline = datetime.strptime(deadline, '%d-%m-%Y').date() if deadline != "None" else None
                tasks.append({'task': task, 'completed': completed, 'deadline': deadline})
            return tasks
    return []
def main():
    tasks = load_tasks()
    menu_options = {1: "add_task",2: "view_tasks",3: "mark_task_completed",4: "remove_task",5: "edit_task",6: lambda tasks: [print("Saving tasks and exiting To-Do List. Goodbye!"), save_tasks(tasks), exit()]}
    while True:
        clear_screen()
        display_menu()
        choice = input("Enter your choice: ")
        if choice in menu_options:
            menu_options[choice](tasks)
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()