import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import add_task, edit_task, delete_task, complete_task
from tkcalendar import DateEntry
import delete_column
from datetime import datetime

# **Open Add Column Window**
def open_add_column():
    add_col_win = tk.Toplevel(root)
    add_col_win.title("Add New Column")

    tk.Label(add_col_win, text="Column Name:").grid(row=0, column=0)
    col_name_entry = tk.Entry(add_col_win)
    col_name_entry.grid(row=0, column=1)

    tk.Label(add_col_win, text="Column Type:").grid(row=1, column=0)
    col_type_combo = ttk.Combobox(add_col_win, values=["TEXT", "INTEGER", "FLOAT", "DROPDOWN"])
    col_type_combo.grid(row=1, column=1)

    tk.Label(add_col_win, text="Dropdown Values (if applicable):").grid(row=2, column=0)
    dropdown_values_entry = tk.Entry(add_col_win)
    dropdown_values_entry.grid(row=2, column=1)

    def add_column():
        col_name = col_name_entry.get().strip()
        col_type = col_type_combo.get().upper()
        dropdown_values = dropdown_values_entry.get().split(",") if col_type == "DROPDOWN" else None

        if not col_name:
            messagebox.showerror("Error", "Column name cannot be empty!")
            return

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(tasks)")
        existing_columns = [col[1] for col in cursor.fetchall()]

        if col_name not in existing_columns:
            cursor.execute(f"ALTER TABLE tasks ADD COLUMN {col_name} {col_type}")
            conn.commit()
            messagebox.showinfo("Success", f"Column '{col_name}' added successfully!")

            if dropdown_values:
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {col_name}_options (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        value TEXT UNIQUE NOT NULL
                    )
                ''')
                for value in dropdown_values:
                    cursor.execute(f"INSERT OR IGNORE INTO {col_name}_options (value) VALUES (?)", (value.strip(),))
                conn.commit()
                messagebox.showinfo("Success", f"Dropdown options for '{col_name}' added.")

        else:
            messagebox.showwarning("Warning", f"Column '{col_name}' already exists.")

        conn.close()
        add_col_win.destroy()
        refresh_task_table()

    tk.Button(add_col_win, text="Add Column", command=add_column).grid(row=3, column=1)

# **Refresh Task Table**
def refresh_task_table():
    """Refresh the task list and update columns dynamically."""
    for row in task_tree.get_children():
        task_tree.delete(row)

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in cursor.fetchall()]

    # Update treeview columns dynamically
    task_tree["columns"] = columns
    for col in columns:
        task_tree.heading(col, text=col.capitalize())

    conn.close()
    load_tasks()

# **Load Tasks from Database**
def load_tasks(filter_text=""):
    for row in task_tree.get_children():
        task_tree.delete(row)

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in cursor.fetchall()]

    query = f"SELECT * FROM tasks WHERE {' OR '.join([f'{col} LIKE ?' for col in columns])} ORDER BY due_date ASC"
    cursor.execute(query, tuple([f"%{filter_text}%"] * len(columns)))

    tasks = cursor.fetchall()
    conn.close()

    for task in tasks:
        task_tree.insert("", "end", values=task)

# **Delete Column**
def open_delete_column_window():
    delete_win = tk.Toplevel(root)
    delete_win.title("Delete Column")

    tk.Label(delete_win, text="Enter Column Name to Delete:").pack(pady=5)
    column_entry = tk.Entry(delete_win)
    column_entry.pack(pady=5)

    def delete_column_action():
        column_name = column_entry.get().strip()
        if column_name:
            delete_column.delete_column(column_name)
            delete_win.destroy()
            refresh_task_table()
        else:
            messagebox.showerror("Error", "Please enter a column name.")

    tk.Button(delete_win, text="Delete", command=delete_column_action).pack(pady=10)

def open_add_task():
    """Opens the Add Task window."""
    add_win = tk.Toplevel(root)
    add_win.title("Add Task")

    tk.Label(add_win, text="Task Title:").grid(row=0, column=0)
    title_entry = tk.Entry(add_win)
    title_entry.grid(row=0, column=1)

    tk.Label(add_win, text="Description:").grid(row=1, column=0)
    desc_entry = tk.Entry(add_win)
    desc_entry.grid(row=1, column=1)

    tk.Label(add_win, text="Due Date:").grid(row=2, column=0)
    due_date_entry = DateEntry(add_win, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
    due_date_entry.grid(row=2, column=1)

    tk.Label(add_win, text="Priority:").grid(row=3, column=0)
    priority_combo = ttk.Combobox(add_win, values=["Low", "Medium", "High"])
    priority_combo.grid(row=3, column=1)

    tk.Label(add_win, text="Status:").grid(row=4, column=0)
    status_combo = ttk.Combobox(add_win, values=["Pending", "Completed"])
    status_combo.grid(row=4, column=1)

    # ✅ Correctly Indented `save_task()`
    def save_task():
        """Saves a new task into the database and retrieves the Task ID."""
        title = title_entry.get().strip()
        desc = desc_entry.get().strip()
        due_date = due_date_entry.get()
        priority = priority_combo.get()
        status = status_combo.get()

        if not title:
            messagebox.showerror("Error", "Title cannot be empty!")
            return

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        # ✅ Insert task and retrieve the generated Task ID
        cursor.execute("INSERT INTO tasks (title, description, due_date, priority, status) VALUES (?, ?, ?, ?, ?)",
                       (title, desc, due_date, priority, status))
        task_id = cursor.lastrowid  # ✅ Fix: Retrieve inserted task ID
        conn.commit()
        conn.close()

        print(f"Task Added: ID = {task_id}, Title = {title}")  # Debugging Output

        messagebox.showinfo("Success", f"Task added successfully! Task ID: {task_id}")  # ✅ Show Task ID
        add_win.destroy()
        load_tasks()  # ✅ Refresh table

    tk.Button(add_win, text="Save", command=save_task).grid(row=5, column=1)


def delete_selected_task():
    """Deletes the selected task from the database."""
    selected_item = task_tree.selection()  # Get selected row ID(s)
    if selected_item:
        selected_row = selected_item[0]  # Get the first selected row
        task_values = task_tree.item(selected_row, "values")  # Extract values from row

        if task_values and len(task_values) > 0:
            task_id = task_values[0]  # Assuming the first column is Task ID
            print(f"Deleting Task ID: {task_id}")  # Debugging Output
            delete_task.delete_task(task_id)  # Calls delete_task script
            load_tasks()
        else:
            messagebox.showwarning("Warning", "Invalid task selection or no task ID found.")
    else:
        messagebox.showwarning("Warning", "No task selected.")

def complete_selected_task():
    """Marks the selected task as Completed."""
    selected_item = task_tree.selection()  # Get selected row ID(s)
    if selected_item:
        selected_row = selected_item[0]  # Get the first selected row
        task_values = task_tree.item(selected_row, "values")  # Extract values from row

        if task_values and len(task_values) > 0:
            task_id = task_values[0]  # Assuming the first column is Task ID
            print(f"Completing Task ID: {task_id}")  # Debugging Output
            complete_task.complete_task(task_id)  # Calls complete_task script
            load_tasks()
        else:
            messagebox.showwarning("Warning", "Invalid task selection or no task ID found.")
    else:
        messagebox.showwarning("Warning", "No task selected.")


# **List Columns**
def list_columns():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()
    return columns

def open_columns_window():
    columns = list_columns()
    col_win = tk.Toplevel(root)
    col_win.title("Table Columns")
    for idx, col in enumerate(columns):
        tk.Label(col_win, text=f"{idx+1}. {col}").pack(pady=2)

# **Refresh Table**
def refresh_table():
    load_tasks()

# **Clock Function**
def update_clock():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clock_label.config(text=now)
    root.after(1000, update_clock)

# **Tkinter UI Setup**
root = tk.Tk()
root.title("Task Manager")
root.geometry("900x500")

# **Top Frame (Title & Clock)**
top_frame = tk.Frame(root, padx=10, pady=5, bg="lightblue")
top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

title_label = tk.Label(top_frame, text="Task Management", font=("Arial", 16, "bold"), bg="lightblue")
title_label.grid(row=0, column=0, padx=10, sticky="w")

clock_label = tk.Label(top_frame, font=("Arial", 14), bg="lightblue")
clock_label.grid(row=0, column=1, padx=10, sticky="e")
update_clock()

separator = ttk.Separator(root, orient="horizontal")
separator.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

# **Left Frame (Buttons)**
left_frame = tk.Frame(root, width=200, padx=10, pady=10, bg="lightgray")
left_frame.grid(row=2, column=0, sticky="ns")

# **Right Frame (Task List)**
right_frame = tk.Frame(root, width=700, padx=10, pady=10)
right_frame.grid(row=2, column=1, sticky="nsew")

# **Buttons**
# **Buttons (Fixed)**
tk.Button(left_frame, text="Add Task", command=open_add_task, width=20, bg="white").pack(pady=5)  # ✅ FIXED
tk.Button(left_frame, text="Delete Task", command=delete_selected_task, width=20, height=1, bg="white").pack(pady=5, ipady=2)
tk.Button(left_frame, text="Complete Task", command=complete_selected_task, width=20, height=1, bg="white").pack(pady=5, ipady=2)
tk.Button(left_frame, text="Add Column", command=open_add_column, width=20, bg="white").pack(pady=5)
tk.Button(left_frame, text="Delete Column", command=open_delete_column_window, width=20, bg="white").pack(pady=5)
tk.Button(left_frame, text="List Columns", command=open_columns_window, width=20, bg="white").pack(pady=5)
tk.Button(left_frame, text="Refresh", command=refresh_table, width=20, bg="white").pack(pady=5)

# **Search Field (Fix: Use pack() instead of grid())**
search_entry = tk.Entry(left_frame, width=22)
search_entry.pack(pady=5)  # ✅ FIXED: Changed from grid() to pack()
tk.Button(left_frame, text="Search Task", command=lambda: print("Search"), width=20, bg="white").pack(pady=5)


# **Task List (Right Frame)**
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(tasks)")
columns = [col[1] for col in cursor.fetchall()]
conn.close()

task_tree = ttk.Treeview(right_frame, columns=columns, show="headings")

for col in columns:
    task_tree.heading(col, text=col.capitalize())

task_tree.grid(row=0, column=0, sticky="nsew")

# **Fix Grid Layout Issue**
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# **Run Tkinter main loop**
root.mainloop()