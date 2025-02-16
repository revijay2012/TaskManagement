import sqlite3
from tkinter import messagebox

def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Task deleted successfully!")
