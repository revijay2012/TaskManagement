import sqlite3
from tkinter import messagebox

def add_note(task_id, note):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO task_notes (task_id, note) VALUES (?, ?)", (task_id, note))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Note added successfully!")

def get_notes(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT created_at, note FROM task_notes WHERE task_id=? ORDER BY created_at DESC", (task_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes
