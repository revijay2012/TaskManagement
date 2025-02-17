import sqlite3

def cleanup_invalid_tasks():
    """Deletes tasks with invalid (None or empty) IDs."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # ✅ Delete tasks where ID is NULL or empty
    cursor.execute("DELETE FROM tasks WHERE id IS NULL OR id = ''")

    conn.commit()
    conn.close()

    print("Invalid tasks deleted successfully.")

# Run this once to clean up the database
cleanup_invalid_tasks()
