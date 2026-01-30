import sqlite3

def create_db():
    # This creates the diary.db file automatically
    connection = sqlite3.connect('diary.db')
    cursor = connection.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
        )
    ''')

    # Create the entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            primary_mood TEXT,
            confidence REAL,
            entry_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    connection.commit()
    connection.close()
    print("Success! diary.db has been created with all necessary tables.")

if __name__ == "__main__":
    create_db()