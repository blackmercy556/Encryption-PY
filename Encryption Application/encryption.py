import sqlite3
from cryptography.fernet import Fernet
from getpass import getpass


def key_storage(e_file, key):
    conn = sqlite3.connect("key.db")
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS file_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT UNIQUE,
            key TEXT
        )
    ''')

    cur.execute('''
        INSERT OR REPLACE INTO file_keys (file_name, key) VALUES (?, ?)
    ''', (e_file + ".encrypted", key.decode()))
    
    conn.commit()
    conn.close()


def key_decryption(e_file):
    conn = sqlite3.connect('key.db')
    c = conn.cursor()
    
    c.execute('SELECT key FROM file_keys WHERE file_name = ?', (e_file + ".encrypted",))
    result = c.fetchone()
    conn.close()

    if result:
        return result[0].encode()  # Convert from string back to bytes
    return None


def process_file(e_file, encrypt_decrypt, key):
    try:
        if encrypt_decrypt == "E":
            cipher = Fernet(key)

            with open(e_file, 'rb') as ef:
                data = ef.read()

            edata = cipher.encrypt(data)

            with open(e_file + ".encrypted", 'wb') as ef:
                ef.write(edata)

            print(f"File encrypted and saved as {e_file}.encrypted")
            key_storage(e_file, key)

        elif encrypt_decrypt == "D":
            key_from_db = key_decryption(e_file)

            if key_from_db is None:
                print(f"No key found for file '{e_file}'.")
                return

            cipher = Fernet(key_from_db)

            with open(e_file + ".encrypted", 'rb') as ef:
                edata = ef.read()

            data = cipher.decrypt(edata)

            with open(e_file + ".decrypted", 'wb') as df:
                df.write(data)

            print(f"File decrypted and saved as {e_file}.decrypted")

        else:
            print("Invalid choice. Please enter 'E' or 'D'.")

    except FileNotFoundError:
        print(f"File '{e_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    key = Fernet.generate_key()
    e_file = ""  # Initialize before using in the loop

    while e_file.lower() != 'exit':
        e_file = input("What file do you want to encrypt/decrypt? Type 'exit' to escape: ")

        if e_file.lower() == 'exit':
            break

        encrypt_decrypt = input("Do you want to encrypt or decrypt? (E/D): ").upper()

        if encrypt_decrypt not in ["E", "D"]:
            print("Invalid choice. Please enter 'E' for encryption or 'D' for decryption.")
            continue

        process_file(e_file, encrypt_decrypt, key)
    

if __name__ == "__main__":
    main()
