# 📝 Streamlit To-Do App

A simple and interactive To-Do List application built using Streamlit. Users can add, view, update, and remove tasks, all stored locally in a text file.

## Features

- ✅ Add new tasks
- 📋 View existing tasks
- ✏️ Update selected tasks
- ❌ Remove completed or unwanted tasks
- 💾 Persistent storage using `tasks.txt`

## Requirements

- Python 3.7+
- Streamlit

Install dependencies:
```bash
pip install streamlit

## How to Run

1. Clone the repository or download the script:
  ```bash
  git clone https://github.com/your-username/streamlit-todo-app.git
  cd streamlit-todo-app

2. Run the app:
   ```bash
   streamlit run app.py


3. Use the dropdown to select a task operation:
  Add Task
  View Tasks
  Update Task
  Remove Task


## Project Structure
streamlit-todo-app/
├── app.py
├── tasks.txt  # Automatically created after adding tasks
└── README.md

## Notes

Tasks are stored in a plain text file (tasks.txt) in the same directory.
The app uses basic Streamlit widgets like selectbox, text_input, and button.
