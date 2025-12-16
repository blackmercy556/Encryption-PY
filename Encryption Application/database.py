import sqlite3

def select_statement():
    conn = sqlite3.connect('key.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM file_keys')
    rows = c.fetchall()

    for row in rows:
        print(row)
    
    conn.close()
    return rows

if __name__ == "__main__": # Call this first to ensure the table exists
    select_statement()
