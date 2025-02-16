import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import add_task, edit_task, delete_task, complete_task

# Load Tasks from Database
def load_tasks(filter_text=""):
    for row in task_tree.get_children():
        task_tree.delete(row)

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Fetch all columns dynamically
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in cursor.fetchall()]

    # Search query
    query = f"SELECT * FROM tasks WHERE {' OR '.join([f'{col} LIKE ?' for col in columns])} ORDER BY due_date ASC"
    cursor.execute(query, tuple([f"%{filter_text}%"] * len(columns)))

    tasks = cursor.fetchall()
    conn.close()

    for task in tasks:
        task_tree.insert("", "end", values=task)

# Open Add Task Window
def open_add_task():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Fetch column names dynamically
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in cursor.fetchall()]

    add_win = tk.Toplevel(root)
    add_win.title("Add Task")

    entries = {}
    row_idx = 0

    for col in columns:
        if col == "id":  # Skip ID column
            continue

        tk.Label(add_win, text=f"{col.capitalize()}:").grid(row=row_idx, column=0)

        # **Set predefined dropdowns for Priority & Status**
        if col == "priority":
            entry = ttk.Combobox(add_win, values=["Low", "Medium", "High"])
            entry.current(0)  # Default to "Low"
        elif col == "status":
            entry = ttk.Combobox(add_win, values=["Pending", "Completed"])
            entry.current(0)  # Default to "Pending"
        else:
            # Check if column has a dropdown list
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{col}_options'")
            dropdown_exists = cursor.fetchone()

            if dropdown_exists:
                cursor.execute(f"SELECT value FROM {col}_options")
                options = [row[0] for row in cursor.fetchall()]
                entry = ttk.Combobox(add_win, values=options)
            else:
                entry = tk.Entry(add_win)

        entry.grid(row=row_idx, column=1)
        entries[col] = entry
        row_idx += 1

    conn.close()

    def save_task():
        task_data = {col: entries[col].get() for col in entries}

        # **Extract only expected fields for add_task()**
        allowed_fields = ["title", "description", "due_date", "priority", "status"]
        filtered_data = {key: task_data[key] for key in allowed_fields if key in task_data}

        # **Insert the main task (returns the task ID)**
        task_id = add_task.add_task(**filtered_data)

        # **Save dynamic fields separately (like "AssignTo")**
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        for key, value in task_data.items():
            if key not in allowed_fields:  # **Handle extra fields**
                cursor.execute(f"UPDATE tasks SET {key} = ? WHERE id = ?", (value, task_id))

        conn.commit()
        conn.close()

        load_tasks()
        add_win.destroy()

    tk.Button(add_win, text="Save", command=save_task).grid(row=row_idx, column=1)

# Delete Task
def delete_selected_task():
    selected_item = task_tree.selection()
    if selected_item:
        task_id = task_tree.item(selected_item, "values")[0]
        delete_task.delete_task(task_id)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected.")

# Complete Task
def complete_selected_task():
    selected_item = task_tree.selection()
    if selected_item:
        task_id = task_tree.item(selected_item, "values")[0]
        complete_task.complete_task(task_id)
        load_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected.")

# Search Tasks
def search_task():
    filter_text = search_entry.get()
    load_tasks(filter_text)

# Tkinter UI
root = tk.Tk()
root.title("Task Manager")
root.geometry("900x500")

# **Left Frame for Buttons**
left_frame = tk.Frame(root, width=200, padx=10, pady=10, bg="lightgray")
left_frame.pack(side="left", fill="y")

# **Right Frame for Task List**
right_frame = tk.Frame(root, width=700, padx=10, pady=10)
right_frame.pack(side="right", fill="both", expand=True)

# **Buttons on Left Frame**
tk.Button(left_frame, text="Add Task", command=open_add_task, width=20, bg="white").pack(pady=5)
tk.Button(left_frame, text="Delete Task", command=delete_selected_task, width=20, bg="white").pack(pady=5)
tk.Button(left_frame, text="Complete Task", command=complete_selected_task, width=20, bg="white").pack(pady=5)

# **Search Field**
search_entry = tk.Entry(left_frame, width=22)
search_entry.pack(pady=5)
tk.Button(left_frame, text="Search Task", command=search_task, width=20, bg="white").pack(pady=5)

# **Task List (Right Side)**
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(tasks)")
columns = [col[1] for col in cursor.fetchall()]  # Fetch all column names dynamically
conn.close()

task_tree = ttk.Treeview(right_frame, columns=columns, show="headings")

# Set column headings dynamically
for col in columns:
    task_tree.heading(col, text=col.capitalize())

task_tree.pack(fill="both", expand=True)

# Load Tasks Initially
load_tasks()

root.mainloop()
