import sqlite3
from tkinter import messagebox

def edit_task(task_id, title, description, due_date, priority, status):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title=?, description=?, due_date=?, priority=?, status=? WHERE id=?",
                   (title, description, due_date, priority, status, task_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Task updated successfully!")
