import sqlite3

def connect_db():
    """Creates or connects to the tasks database and ensures tables exist."""
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    # ✅ Create Tasks table with AUTO-INCREMENTING ID
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')),
            status TEXT CHECK(status IN ('Pending', 'Completed')) DEFAULT 'Pending'
        )
    ''')

    # ✅ Create Task Notes table with a foreign key to tasks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            note TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
        )
    ''')

    # ✅ Create an Index for faster lookup on task_id in task_notes
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_task_notes_task_id ON task_notes (task_id);
    ''')

    conn.commit()
    conn.close()

# Run this function once to ensure tables exist
connect_db()

print("Database connected, tables created if not exists.")
p