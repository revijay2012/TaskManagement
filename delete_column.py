import sqlite3

def delete_column(column_name):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Get existing column names
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in cursor.fetchall()]

    # Check if column exists
    if column_name not in columns:
        print(f"Column '{column_name}' does not exist in the 'tasks' table.")
        conn.close()
        return

    # Create a new table without the column
    new_columns = [col for col in columns if col != column_name]
    new_columns_str = ", ".join(new_columns)

    cursor.execute(f"CREATE TABLE tasks_new AS SELECT {new_columns_str} FROM tasks")
    
    # Drop the old table and rename the new one
    cursor.execute("DROP TABLE tasks")
    cursor.execute("ALTER TABLE tasks_new RENAME TO tasks")

    conn.commit()
    conn.close()
    print(f"Column '{column_name}' has been deleted successfully.")
