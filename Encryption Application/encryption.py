import sqlite3
from cryptography.fernet import Fernet
from getpass import getpass


def key_storage(e_file, cipher):
    """
    Store the encryption key in the database.
    Parameters:
    e_file (str): The path to the file for which the key is stored.
    cipher (Fernet): A Fernet cipher object containing the key to be stored.
    """
    conn = sqlite3.connect("key.db")
    cur = conn.cursor()

    
    # Store the encryption key in the database
    cur.execute('''
        INSERT OR REPLACE INTO file_keys (file_name, key) VALUES (?, ?)
    ''', (e_file + ".encrypted", cipher))
    
    conn.commit()
    conn.close()


def key_decryption(e_file):
    """
    Retrieve the encryption key from the database and decode it.

    Parameters:
    e_file (str): The name of the file for which to retrieve the key.

    Returns:
    bytes: The decoded encryption key, or None if not found.
    """
    conn = sqlite3.connect('key.db')
    c = conn.cursor()
    
    # Execute the SELECT statement
    c.execute('SELECT key FROM file_keys WHERE file_name = ?', (e_file))
    
    # Fetch results
    result = c.fetchone()
    
    # Close the connection
    conn.close()

    return result



def process_file(e_file, encrypt_decrypt, cipher):
    """
    Encrypt or decrypt a file based on user input.

    Parameters:
    e_file (str): The path to the file to be processed.
    encrypt_decrypt (str): 'E' for encryption, 'D' for decryption.
    cipher (Fernet): A Fernet cipher object for encryption/decryption.
    """
    try:
        if encrypt_decrypt == "E":
            # Encrypt the file
            with open(e_file, 'rb') as ef:
                data = ef.read()  # Read the entire file content
                edata = cipher.encrypt(data)  # Encrypt the data

            # Save the encrypted data to a new file
            with open(e_file + ".encrypted", 'wb') as ef:
                ef.write(edata)
            print(f"File encrypted and saved as {e_file}.encrypted")
            
            # Store the key in the database
            key_storage(e_file, cipher)

        elif encrypt_decrypt == "D":
            # Retrieve the key for decryption
            key_bytes = key_decryption(e_file)  
            
            if key_bytes is None:
                print(f"No key found for file '{e_file}'.")
                return

            # Read the encrypted data
            with open(e_file + ".encrypted", 'rb') as ef:
                edata = ef.read()
            
            # Save the decrypted data to a new file
            with open(e_file + ".decrypted", 'wb') as df:
                data = cipher.decrypt(edata)  # Decrypt the data
                df.write(data)
            print(f"File decrypted and saved as {e_file}.decrypted")

        else:
            print("Invalid choice. Please enter 'E' for encryption or 'D' for decryption.")
    except FileNotFoundError:
        print(f"File '{e_file}' not found. Please input a valid file from this directory.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main function to handle user inputs and call the file processing function.
    """
    key = Fernet.generate_key()  # Generate a new key
    cipher = Fernet(key)  # Create a Fernet cipher object using the generated key

    password = "Jovee2118"

    e_file = ""  # Initialize the file name variable
    
    while e_file.lower() != 'exit':
        e_file = input("What file do you want to encrypt/decrypt? Type 'exit' to Escape: ")
        
        if e_file.lower() == 'exit':
            break
        
        encrypt_decrypt = input("Do you want to encrypt or decrypt? (E/D): ").upper()
        
        if encrypt_decrypt not in ["E", "D"]:
            print("Invalid choice. Please enter 'E' for encryption or 'D' for decryption.")
            continue

        password_input = getpass("Enter Password: ")

        if password_input != password:
            print("Wrong Password. Goodbye.")
            break
            
        process_file(e_file, encrypt_decrypt, cipher)


# Check if this script is being run directly and not imported as a module
if __name__ == "__main__":
    main()
