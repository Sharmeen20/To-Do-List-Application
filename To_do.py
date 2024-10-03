from datetime import datetime
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Function to display the menu
def display_menu():
    print("\n---- To-Do List ----")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Completed")
    print("4. Remove Task")
    print("5. Exit")

# Function to add a task
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
    save_tasks(tasks)
    print(f"Task '{task}' added successfully!")

# Function to view all tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks to show!")
    else:
        print("\nYour Tasks:")
        # for idx, task in enumerate(tasks, 1):
        #     print(f"{idx}. {task}")
            
        for idx, task_info in enumerate(tasks, 1):
            task_status = "[✔]" if task_info['completed'] else "[ ]"
            deadline = f"(Deadline: {task_info['deadline']})" if task_info['deadline'] else ""
            print(f"{idx}. {task_status} {task_info['task']} {deadline}")


# Function to mark a task as completed
def mark_task_completed(tasks):
    if not tasks:
        print("No tasks to mark as completed!")
    else:
        view_tasks(tasks)
        try:
            task_num = int(input("Enter the task number to mark as completed: "))
            if 0 < task_num <= len(tasks):
                tasks[task_num - 1]['completed'] = True
                save_tasks(tasks)
                print(f"Task '{tasks[task_num - 1]['task']}' marked as completed!")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")


# Function to remove a task
def remove_task(tasks):
    if not tasks:
        print("No tasks to remove!")
    else:
        view_tasks(tasks)
        try:
            task_num = int(input("Enter the task number to remove: "))
            if 0 < task_num <= len(tasks):
                confirm = input(f"Are you sure you want to remove task '{tasks[task_num - 1]['task']}'? (y/n): ")
                if confirm.lower() == 'y':
                   removed_task = tasks.pop(task_num - 1)
                   save_tasks(tasks)
                   print(f"Task '{removed_task}' removed successfully!")
                else:
                    print("Task removal canceled.")
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
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

# Function to save tasks to a file
def save_tasks(tasks):
    with open("tasks.txt", "w") as file:
        for task_info in tasks:
            task = task_info['task']
            completed = str(task_info['completed'])
            deadline = task_info['deadline'].strftime('%d-%m-%Y') if task_info['deadline'] else "None"
            file.write(f"{task},{completed},{deadline}\n")

# Function to load tasks from a file
def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            tasks = []
            for line in file:
                task, completed, deadline = line.strip().split(',')
                completed = completed == 'True'
                deadline = datetime.strptime(deadline, '%d-%m-%Y').date() if deadline != "None" else None
                tasks.append({'task': task, 'completed': completed, 'deadline': deadline})
        return tasks
    return []

# Main function
def main():
    tasks = load_tasks()
    
    while True:
         clear_screen()
         display_menu()
         choice = input("Enter your choice: ")
        
         if choice == '1':
            add_task(tasks)
         elif choice == '2':
            view_tasks(tasks)
         elif choice == '3':
            mark_task_completed(tasks)
         elif choice == '4':
            remove_task(tasks)
         elif choice == '5':
             print("Saving tasks and exiting To-Do List. Goodbye!")
             save_tasks(tasks)
             break
         else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()