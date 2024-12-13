import requests
import hashlib
import sys
import string
import random
from datetime import datetime
from cryptography.fernet import Fernet
from colorama import init, Fore, Style
import toml
import os
import streamlit as st

init()  # Initialize colorama

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)):
            return password

def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Password should be at least 12 characters long")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Include uppercase letters")
        
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Include lowercase letters")
        
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Include numbers")
        
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Include special characters")
    
    return score, feedback

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pawned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return password_leaks_count(response, tail)

def load_key():
    """Load encryption key from various sources"""
    try:
        # For Streamlit Cloud deployment
        if 'streamlit' in sys.modules:
            try:
                return st.secrets["fernet_key"]
            except KeyError:
                st.error("Streamlit secrets not configured properly")
                st.stop()
                
        # For local development
        if os.path.exists("secret.key"):
            with open("secret.key", "rb") as key_file:
                return key_file.read()
        
        if os.path.exists("secrets.toml"):
            secrets = toml.load("secrets.toml")
            return secrets["fernet_key"].encode()
            
        raise FileNotFoundError("No encryption key found")
            
    except Exception as e:
        if 'streamlit' in sys.modules:
            st.error(f"Error loading encryption key: {str(e)}")
            st.stop()
        else:
            print(Fore.RED + f"Error loading encryption key: {str(e)}" + Style.RESET_ALL)
            sys.exit(1)

def encrypt_message(message):
    try:
        key = load_key()
        f = Fernet(key)
        return f.encrypt(message.encode())
    except Exception as e:
        print(Fore.RED + f"Encryption error: {str(e)}" + Style.RESET_ALL)
        return None

def decrypt_message(encrypted_message):
    try:
        key = load_key()
        f = Fernet(key)
        return f.decrypt(encrypted_message).decode()
    except Exception as e:
        print(Fore.RED + f"Decryption error: {str(e)}" + Style.RESET_ALL)
        return None

def log_password_check(password, count, strength_score):
    try:
        with open('password_history.txt', 'ab') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"{timestamp} - Password: {password} - Times found: {count} - Strength: {strength_score}/5"
            encrypted_log = encrypt_message(log_entry)
            if encrypted_log:
                f.write(encrypted_log + b'\n')
    except Exception as e:
        print(Fore.RED + f"Logging error: {str(e)}" + Style.RESET_ALL)

def authenticate_user():
    try:
        username = input("Enter username: ")
        password = input("Enter password: ")
        # In a real application, these should be stored securely
        if username == "admin" and password == "password123":
            print(Fore.GREEN + "Authentication successful!" + Style.RESET_ALL)
            return True
        print(Fore.RED + "Authentication failed!" + Style.RESET_ALL)
        return False
    except Exception as e:
        print(Fore.RED + f"Authentication error: {str(e)}" + Style.RESET_ALL)
        return False

def main():
    try:
        if not authenticate_user():
            return 'Authentication failed! Exiting...'
        
        print(Fore.CYAN + "=== Password Security Checker ===" + Style.RESET_ALL)
        print("1. Check passwords from file")
        print("2. Generate strong password")
        print("3. Check single password")
        choice = input("Select an option (1-3): ")

        if choice == '1':
            try:
                # Changed from 'rb' to 'r' for plain text reading
                with open('passwords.txt', 'r') as file:
                    passwords = file.readlines()
                for password in passwords:
                    password = password.strip()
                    if password:  # Skip empty lines
                        print(f"\nChecking password: {password}")
                        process_password(password)
            except FileNotFoundError:
                print(Fore.RED + "Error: passwords.txt not found" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error reading passwords: {str(e)}" + Style.RESET_ALL)
        
        elif choice == '2':
            try:
                length = int(input("Enter desired password length (minimum 12): "))
                length = max(12, length)
                new_password = generate_strong_password(length)
                print(Fore.GREEN + f"\nGenerated strong password: {new_password}" + Style.RESET_ALL)
                process_password(new_password)
            except ValueError:
                print(Fore.RED + "Please enter a valid number" + Style.RESET_ALL)
        
        elif choice == '3':
            password = input("Enter password to check: ")
            process_password(password)
        
        else:
            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)

        return 'done!'
    
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}" + Style.RESET_ALL)
        return 'error!'

def process_password(password):
    try:
        count = pawned_api_check(password)
        strength_score, feedback = check_password_strength(password)
        
        if count:
            print(Fore.RED + f'❌ Password was found {count} times... you should change it!' + Style.RESET_ALL)
        else:
            print(Fore.GREEN + f'✓ Password was NOT found. Carry on!' + Style.RESET_ALL)
        
        print(Fore.YELLOW + f'Password strength: {strength_score}/5' + Style.RESET_ALL)
        if feedback:
            print(Fore.YELLOW + "Improvements needed:" + Style.RESET_ALL)
            for suggestion in feedback:
                print(f"- {suggestion}")
        
        log_password_check(password, count, strength_score)
        print("-" * 50)
    except Exception as e:
        print(Fore.RED + f"Error processing password: {str(e)}" + Style.RESET_ALL)

if __name__ == '__main__':
    sys.exit(main())
