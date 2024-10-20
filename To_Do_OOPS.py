import os
import json
from datetime import datetime, timedelta

class Task:
    def __init__(self, description, due_date=None, priority="Medium", completed=False):
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data["description"])
        task.due_date = data["due_date"]
        task.priority = data["priority"]
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        return task

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.filename = "tasks.json"
        self.load_tasks()

    def add_task(self):
        description = input("Enter task description: ")
        due_date = input("Enter due date (YYYY-MM-DD) or press Enter for no due date: ")
        priority = input("Enter priority (High/Medium/Low) [Medium]: ").capitalize() or "Medium"
        
        if due_date:
            try:
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date().isoformat()
            except ValueError:
                print("Invalid date format. Task will be created without a due date.")
                due_date = None

        task = Task(description, due_date, priority)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task '{description}' added successfully!")

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
        for idx, task in enumerate(self.tasks, 1):
            status = "✓" if task.completed else "✗"
            due = f"Due: {task.due_date}" if task.due_date else "No due date"
            print(f"{idx}. [{status}] {task.description} - Priority: {task.priority}, {due}")

    def remove_task(self):
        if not self.tasks:
            print("No tasks to remove!")
            return

        self.view_tasks()
        try:
            task_num = int(input("Enter the task number to remove: "))
            if 0 < task_num <= len(self.tasks):
                removed_task = self.tasks.pop(task_num - 1)
                self.save_tasks()
                print(f"Task '{removed_task.description}' removed successfully!")
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
            task_num = int(input("Enter the task number to mark as completed: "))
            if 0 < task_num <= len(self.tasks):
                task = self.tasks[task_num - 1]
                task.completed = True
                self.save_tasks()
                print(f"Task '{task.description}' marked as completed!")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=2)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task_data) for task_data in data]

    def show_statistics(self):
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task.completed)
        pending_tasks = total_tasks - completed_tasks
        
        print("\nTask Statistics:")
        print(f"Total tasks: {total_tasks}")
        print(f"Completed tasks: {completed_tasks}")
        print(f"Pending tasks: {pending_tasks}")
        
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            print(f"Completion rate: {completion_rate:.2f}%")

        overdue_tasks = sum(1 for task in self.tasks if task.due_date and not task.completed and datetime.strptime(task.due_date, "%Y-%m-%d").date() < datetime.now().date())
        print(f"Overdue tasks: {overdue_tasks}")

def display_menu():
    print("\n---- To-Do List ----""\n1. Add Task""\n2. View Tasks""\n3. Remove Task""\n4. Mark Task as Completed""\n5. Show Statistics""\n6. Exit")

def main():
    todo_list = ToDoList()
    menu_options = {'1': todo_list.add_task, '2': todo_list.view_tasks, '3': todo_list.remove_task,
                    '4': todo_list.mark_completed, '5': todo_list.show_statistics,
                    '6': lambda: [print("Exiting To-Do List. Goodbye!"), exit()]}
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        (menu_options.get(choice, lambda: print("Invalid choice! Please try again.")))()

if __name__ == "__main__":
    main()