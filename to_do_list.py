class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f'Task added: "{task}"')

    def view_tasks(self):
        if not self.tasks:
            print("No tasks in the list.")
        else:
            print("To-Do List:")
            for index, task in enumerate(self.tasks, start=1):
                print(f"{index}. {task}")

    def remove_task(self, task_number):
        try:
            removed_task = self.tasks.pop(task_number - 1)
            print(f'Task removed: "{removed_task}"')
        except IndexError:
            print("Invalid task number.")

def main():
    todo_list = ToDoList()

    while True:
        print("\nOptions:""\n1. Add Task""\n2. View Tasks""\n3. Remove Task""\n4. Exit")

        choice = input("Choose an option (1-4): ")

        options = {
            '1': lambda: todo_list.add_task(input("Enter the task: ")),
            '2': todo_list.view_tasks,
            '3': lambda: todo_list.remove_task(int(input("Enter the task number to remove: "))),
            '4': lambda: [print("Exiting the to-do list application."), exit()]
        }

        options.get(choice, lambda: print("Invalid option. Please choose again."))()

if __name__ == "__main__":
    main()
