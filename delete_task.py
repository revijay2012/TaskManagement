import sqlite3

def delete_task(task_id):
    """Deletes a task from the database."""
    print(f"Attempting to delete task ID: {task_id}")  # Debugging
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(f"Task {task_id} deleted successfully")  # Debugging
