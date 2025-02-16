import sqlite3

def connect_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    
    # Create Tasks table
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

    # Create Task Notes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    conn.commit()
    conn.close()

connect_db()
