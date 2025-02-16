import sqlite3

def add_new_column(column_name, column_type="TEXT", dropdown_values=None):
    """
    Adds a new column to the tasks table if it does not already exist.
    
    Args:
        column_name (str): The name of the new column.
        column_type (str): The type of the column (TEXT, INTEGER, FLOAT).
        dropdown_values (list, optional): If provided, creates a table to store dropdown options.
    """
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # Check if column already exists
    cursor.execute("PRAGMA table_info(tasks)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    if column_name not in existing_columns:
        cursor.execute(f"ALTER TABLE tasks ADD COLUMN {column_name} {column_type}")
        conn.commit()
        print(f"Column '{column_name}' added successfully as {column_type}.")
        
        # If dropdown values are provided, create a separate table for dropdown options
        if dropdown_values:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {column_name}_options (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value TEXT UNIQUE NOT NULL
                )
            ''')
            for value in dropdown_values:
                cursor.execute(f"INSERT OR IGNORE INTO {column_name}_options (value) VALUES (?)", (value,))
            conn.commit()
            print(f"Dropdown options for '{column_name}' added successfully.")
    else:
        print(f"Column '{column_name}' already exists.")

    conn.close()

if __name__ == "__main__":
    print("\n=== Add a New Column to the Tasks Table ===")
    
    col_name = input("Enter the column name: ")
    col_type = input("Enter the column type (TEXT, INTEGER, FLOAT, DROPDOWN): ").upper()
    
    dropdown_values = None
    if col_type == "DROPDOWN":
        values = input("Enter dropdown values (comma-separated): ")
        dropdown_values = values.split(",")
        col_type = "TEXT"  # Store dropdown selections as TEXT in the main table
    
    add_new_column(col_name, col_type, dropdown_values)
