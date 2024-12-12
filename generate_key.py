# from cryptography.fernet import Fernet

# def generate_key():
#     key = Fernet.generate_key()
#     with open("secret.key", "wb") as key_file:
#         key_file.write(key)

# if __name__ == "__main__":
#     generate_key()

from cryptography.fernet import Fernet
import os

def generate_key():
    try:
        # Generate a new Fernet key
        key = Fernet.generate_key()
        
        # Save the key to a file
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
            
        print("Key generated successfully!")
        
    except Exception as e:
        print(f"Error generating key: {str(e)}")

if __name__ == '__main__':
    generate_key()
