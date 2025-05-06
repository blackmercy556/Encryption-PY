import sqlite3


def initialize_database():
    conn = sqlite3.connect('key.db')  # Open or create the database file
    c = conn.cursor()
    
    # Create the table if it doesn't already exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS file_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT UNIQUE,
            key CHAR
        )
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

def select_statement():
    conn = sqlite3.connect('key.db')  # Open or create the database file
    c = conn.cursor()
    
    # Create the table if it doesn't already exist
    c.execute('''
        SELECT * FROM file_keys
    ''')

    rows = c.fetchall()

    for row in rows:
        print(row)
    
    return row


if __name__ == "__main__":
    select_statement()