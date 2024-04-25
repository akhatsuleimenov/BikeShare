import sqlite3

def create_database():
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # SQL query to create a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        age INTEGER,
        class TEXT
    )
    ''')

    # Commit and close connection
    conn.commit()
    conn.close()

    print("Database and table created successfully.")
    
def setup_session_table():
    # Connect to SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # SQL query to create a table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        session_id TEXT PRIMARY KEY,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Commit and close connection
    conn.commit()
    conn.close()

# Run the function to create the database and table
create_database()

# run the function to setup the session table
setup_session_table()
