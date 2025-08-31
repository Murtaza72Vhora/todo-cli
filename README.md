# 📝 Todo CLI

A simple and **friendly command-line to-do list application** built with Python.  
Manage your tasks efficiently directly from the terminal, with features like priority levels, due dates, and persistent storage.

---

## ✨ Features
- ➕ **Add new tasks** with optional priority (Low, Medium, High) and due date  
- 📋 **List tasks** with clear formatting, color-coded priorities, and due dates  
- ✅ **Mark tasks as completed**  
- ❌ **Delete tasks**  
- 💾 **Persistent storage**: tasks are saved in a JSON file (`~/.todo_cli.json`)  
- 🔀 **Task sorting**: undone tasks first, higher priority first, then by ID  

---

## 🛠 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Murtaza72Vhora/todo-cli.git
cd todo-cli
```

2. **Install dependencies** (requires Python 3.10+)
```bash
pip install -r requirements.txt
```

> ⚠️ Make sure you have Python 3.10 or later installed.  

---

## 🚀 Usage

### Add a task
```bash
python todo.py add "Buy groceries" -p 2 -d 2025-09-05
```
- `-p` or `--priority`: 1=Low, 2=Medium, 3=High  
- `-d` or `--due`: Due date in `YYYY-MM-DD` format  

### List tasks
```bash
python todo.py list
python todo.py list --all     # show all tasks
python todo.py list --done    # show only completed tasks
```

### Mark a task as done
```bash
python todo.py done 1
```

### Delete a task
```bash
python todo.py delete 1
```

---

## 🗂 Data Storage

All tasks are stored in a JSON file in your home directory:
```
~/.todo_cli.json
```
This ensures your tasks persist between sessions.

---


## ❤️ Contribution

Feel free to fork this project and submit pull requests!  
Suggestions and improvements are welcome.