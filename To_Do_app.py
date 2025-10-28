import streamlit as st
import os

st.markdown("<h2 style='text-align: center;'>📝 To-Do App</h2>", unsafe_allow_html=True)

task_file = 'tasks.txt'

# Ensure task file exists
if not os.path.exists(task_file):
    open(task_file, 'w').close()

taskbox = st.selectbox('Choose an action:', ['Add Task', 'Update Task', 'Remove Task', 'View Tasks'])

def load_tasks():
    with open(task_file, 'r') as file:
        return [task.strip() for task in file.readlines() if task.strip()]

def save_tasks(tasks):
    with open(task_file, 'w') as file:
        for task in tasks:
            file.write(task + '\n')

if taskbox == 'Add Task':
    add_task = st.text_input('Enter a new task:')
    if st.button("➕ Add Task"):
        if add_task.strip():
            tasks = load_tasks()
            tasks.append(add_task.strip())
            save_tasks(tasks)
            st.success("✅ Task added successfully!")
        else:
            st.error("⚠️ Please enter a valid task.")

elif taskbox == 'View Tasks':
    tasks = load_tasks()
    if tasks:
        st.markdown(f"### 📋 You have {len(tasks)} task(s):")
        for i, task in enumerate(tasks, 1):
            st.write(f"{i}. {task}")
    else:
        st.info("📭 No tasks found.")

elif taskbox == 'Remove Task':
    tasks = load_tasks()
    if tasks:
        task_to_remove = st.selectbox('Select a task to remove:', tasks)
        if st.button("🗑️ Remove Task"):
            tasks = [task for task in tasks if task != task_to_remove]
            save_tasks(tasks)
            st.success(f"✅ Task '{task_to_remove}' removed successfully!")
    else:
        st.info("📭 No tasks to remove.")

elif taskbox == 'Update Task':
    tasks = load_tasks()
    if tasks:
        task_to_update = st.selectbox('Select a task to update:', tasks)
        updated_task = st.text_input('Enter the updated task:')
        if st.button("✏️ Update Task"):
            if updated_task.strip():
                tasks = [updated_task.strip() if task == task_to_update else task for task in tasks]
                save_tasks(tasks)
                st.success(f"✅ Task '{task_to_update}' updated successfully!")
            else:
                st.error("⚠️ Please enter a valid updated task.")
    else:
        st.info("📭 No tasks to update.")
