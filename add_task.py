import sqlite3

def add_task(title, description, due_date, priority, status):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (title, description, due_date, priority, status) VALUES (?, ?, ?, ?, ?)",
                   (title, description, due_date, priority, status))

    task_id = cursor.lastrowid  # ✅ Get the ID of the newly inserted task
    conn.commit()
    conn.close()

    return task_id  # ✅ Return task ID to update extra fields separately
