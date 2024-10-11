import streamlit as st
import os

st.markdown("<h2 style='text-align: center;'>To-Do App</h2>", unsafe_allow_html=True)

taskbox = st.selectbox('Select a task', ['Add Task', 'Update Task', 'Remove Task', 'View Tasks'])

if taskbox == 'Add Task':
    add_task = st.text_input('Enter the task: ')
    if st.button("Submit"):
        if add_task:
            with open('tasks.txt', 'a') as file:
                file.write(add_task + '\n')
            st.success("Task added successfully!")
        else:
            st.error("Please enter some text.")

elif taskbox == 'View Tasks':
    if os.path.exists('tasks.txt'):
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
        if tasks:
            st.write("Tasks:")
            for task in tasks:
                st.write(task.strip())
        else:
            st.write("No tasks found.")
    else:
        st.write("No tasks found.")

elif taskbox == 'Remove Task':
    if os.path.exists('tasks.txt'):
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
        if tasks:
            task_to_remove = st.selectbox('Select a task to remove', [task.strip() for task in tasks])
            if st.button("Remove Task"):
                tasks = [task for task in tasks if task.strip() != task_to_remove]
                with open('tasks.txt', 'w') as file:
                    file.writelines(tasks)
                st.success(f"Task '{task_to_remove}' removed successfully!")
        else:
            st.write("No tasks found.")
    else:
        st.write("No tasks found.")

elif taskbox == 'Update Task':
    if os.path.exists('tasks.txt'):
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
        if tasks:
            task_to_update = st.selectbox('Select a task to update', [task.strip() for task in tasks])
            updated_task = st.text_input('Enter the updated task: ')
            if st.button("Update Task"):
                tasks = [updated_task + '\n' if task.strip() == task_to_update else task for task in tasks]
                with open('tasks.txt', 'w') as file:
                    file.writelines(tasks)
                st.success(f"Task '{task_to_update}' updated successfully!")
        else:
            st.write("No tasks found.")
    else:
        st.write("No tasks found.")