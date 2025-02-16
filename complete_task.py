import sqlite3
from tkinter import messagebox

def complete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Task marked as completed!")
