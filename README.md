# File Encryption Application

Version: v1.0  
Status: Work in Progress

This project is a command-line file encryption tool that uses symmetric-key encryption and stores a unique encryption key per file in a SQLite database.


---

## Features
- Symmetric encryption (same key for encryption and decryption)
- Unique encryption key per file
- SQLite database for key storage
- Cross-platform support (Windows and Linux)
- Non-destructive encryption (original files are preserved)

---

## Installation

### Windows
Place the application inside the Windows folder.

### Linux
Install the application in one of the following locations:
- /opt
- /usr

(depending on your distribution)

---

## Usage

Run the application from the directory containing the files you want to encrypt or decrypt.

Example:


---

## Workflow

### Step 1: Select a File
You will be prompted to enter the name of a file in the current working directory.


Examples:
- Encrypting: test.txt
- Decrypting: test.txt.encrypted

---

### Step 2: Choose an Action
Specify whether you want to encrypt or decrypt the selected file.


E = Encrypt  
D = Decrypt

---

## Output Behavior

### Encryption
- Encrypted file is saved as:
- Original file is not deleted
- Encrypted file is saved in the current working directory
- A unique encryption key is generated and stored in the SQLite database

---

### Decryption
- Decrypted file is saved as:
- Original and encrypted files are not deleted
- The file is decrypted using the key stored in the database
- The file can be re-encrypted with a newly generated key

Note: Encryption key deletion after decryption is currently not working as intended.

---

## Known Issues
- Encryption keys are not properly deleted from the database after decryption
- Key lifecycle management needs improvement

---

## Planned Improvements
- Package all dependencies into a single distributable format
- Fix encryption key deletion after successful decryption
- Improve efficiency of key storage and file handling
- Refactor application structure for maintainability
- Optional graphical user interface (GUI)

---

## Security Notice
This project is intended for learning and experimentation purposes.
It has not been security audited and should not be used to protect sensitive or production data.
