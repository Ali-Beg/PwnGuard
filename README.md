# PwnGuard - Advanced Password Security Tool

> Protect, Generate, and Analyze Your Passwords

A comprehensive password security tool that checks for compromised passwords using the [Have I Been Pwned](https://haveibeenpwned.com/API/v3#PwnedPasswords) API and includes additional security features.

## Features

- Check if passwords have been compromised in data breaches
- Generate strong passwords
- Password strength analysis
- Password history tracking
- Colorful console output for better visibility
- Multiple operation modes (file-based, single password, password generation)
- Interactive Streamlit Dashboard
- Data visualization and analytics
- Real-time password strength monitoring

## Security Measures

- **No Plain Text Storage**: Passwords are never stored in plain text
- **Secure Password History**: All password checks are encrypted before logging
- **K-Anonymity**: Uses HIBP's k-anonymity model (only first 5 chars of hash are sent)
- **SHA-1 Hashing**: Passwords are hashed using SHA-1 before checking
- **Encryption**: Uses Fernet (symmetric encryption) for storing password history
- **Memory Safety**: Sensitive data is cleared from memory after use

## Requirements

- Python 3.x
- Required libraries:
  ```bash
  pip install -r requirements.txt
  ```

## Setup

1. **Create a virtual environment**:
   ```sh
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Deployment

### Local Development

Follow the setup instructions above.

### Streamlit Cloud Deployment

1. Fork this repository to your GitHub account
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Deploy the `streamlit_app.py` file
5. Configure the following secrets in Streamlit Cloud:
   ```toml
   [secrets]
   auth_key = "your_encryption_key"
   ```

## Production Considerations

- Generate a new encryption key for production
- Set up proper authentication for production use
- Configure CORS and security headers
- Use HTTPS for all API calls
- Regular security audits and updates

## How to Use

The application offers four ways to interact:

1. **Command Line Interface**:
   ```bash
   python check_my_passwoed.py
   ```

2. **Graphical User Interface**:
   ```bash
   python gui.py
   ```

3. **Streamlit Dashboard**:
   ```bash
   streamlit run streamlit_app.py
   ```
   The dashboard provides:
   - Interactive password checking
   - Password generation with strength visualization
   - Security analytics dashboard
   - Password strength trends
   - Data breach history

4. **Check passwords from file**:
   - Place passwords in `passwords.txt` (one per line)
   - Run the script and select option 1
   
5. **Generate strong password**:
   - Run the script and select option 2
   - Enter desired password length (minimum 12 characters)
   
6. **Check single password**:
   - Run the script and select option 3
   - Enter the password when prompted

## Password Strength Criteria

Passwords are evaluated based on:
- Length (minimum 12 characters)
- Presence of uppercase letters
- Presence of lowercase letters
- Presence of numbers
- Presence of special characters

## History Tracking

Password checks are logged in `password_history.txt` with:
- Timestamp
- Password
- Number of times found in breaches
- Strength score

## Disclaimer

Use this script responsibly. Do not use it to check passwords that you do not own.