import sqlite3

def complete_task(task_id):
    """Marks a task as completed in the database."""
    print(f"Attempting to mark task ID {task_id} as completed")  # Debugging
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Task {task_id} marked as completed")  # Debugging
