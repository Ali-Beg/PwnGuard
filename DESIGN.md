# PwnGuard - System Design & Architecture

## Overview

PwnGuard is a comprehensive password security tool designed to enhance password security through breach detection, strength analysis, and secure password generation.

## Purpose

The primary purpose of this project is to help users ensure their passwords are secure and have not been compromised in data breaches. It also provides tools to generate strong passwords and evaluate the strength of existing passwords.

## Problems Solved

1. **Compromised Passwords**: Identifies passwords that have been exposed in data breaches.
2. **Weak Passwords**: Generates strong, random passwords that meet security criteria.
3. **Password Strength**: Analyzes and provides feedback on password strength.
4. **Password History**: Logs password checks securely for future reference.

## System Design

### Components

1. **Password Checker**: Checks if passwords have been compromised using the Have I Been Pwned API.
2. **Password Generator**: Generates strong, random passwords.
3. **Password Strength Analyzer**: Evaluates the strength of passwords based on multiple criteria.
4. **Password History Logger**: Logs password checks with encryption for security.
5. **Graphical User Interface (GUI)**: Provides a user-friendly interface for checking and generating passwords.
6. **Streamlit Dashboard**: Provides an interactive web interface with data visualization and analytics.

### Diagram

```plaintext
+-------------------------+
| Password Checker & Gen. |
+-----------+-------------+
            |
    +-------+-------+
    |               |
    v               v
+--------+    +-----------+
|  CLI/  |    | Streamlit |
|  GUI   |    | Dashboard |
+--------+    +-----------+
    |               |
    v               v
+-----------+-------------+
|  Password Checker       |
|  - Uses Have I Been     |
|    Pwned API            |
+-----------+-------------+
            |
            v
+-----------+-------------+
|  Password Generator     |
|  - Generates strong     |
|    passwords            |
+-----------+-------------+
            |
            v
+-----------+-------------+
|  Password Strength      |
|  Analyzer               |
|  - Evaluates password   |
|    strength             |
+-----------+-------------+
            |
            v
+-----------+-------------+
|  Password History       |
|  Logger                 |
|  - Logs password checks |
|    securely             |
+-----------+-------------+
            |
            v
+-----------+-------------+
|  Graphical User         |
|  Interface (GUI)        |
|  - User-friendly        |
|    interface            |
+-------------------------+
```

### How It Works

1. **Password Checker**:
   - Takes a password as input.
   - Hashes the password using SHA-1.
   - Queries the Have I Been Pwned API to check if the password has been compromised.
   - Returns the number of times the password has been found in breaches.

2. **Password Generator**:
   - Generates a random password with a specified length.
   - Ensures the password contains uppercase letters, lowercase letters, numbers, and special characters.

3. **Password Strength Analyzer**:
   - Evaluates the password based on length, presence of uppercase letters, lowercase letters, numbers, and special characters.
   - Provides a strength score and feedback for improvement.

4. **Password History Logger**:
   - Logs password checks with a timestamp, password, breach count, and strength score.
   - Encrypts the log entries to ensure security.

5. **Graphical User Interface (GUI)**:
   - Provides an interface for users to check passwords, generate passwords, and view results.
   - Uses Tkinter for the GUI implementation.

6. **Streamlit Dashboard**:
   - Provides a web-based interface for all password operations
   - Visualizes password strength trends and statistics
   - Displays interactive charts for security metrics
   - Offers real-time password analysis
   - Tracks historical password check data

## Security Architecture

### Password Checking Flow
```plaintext
User Input → SHA-1 Hash → K-Anonymity (first 5 chars) → HIBP API → Result
```

### Password Storage Flow
```plaintext
Password Check → Encrypt with Fernet → Store in History File
```

### Security Measures

1. **Password Handling**:
   - Passwords are never stored in plain text
   - Immediate hashing of passwords
   - Memory clearing after use

2. **API Security**:
   - K-anonymity model for API queries
   - Only first 5 characters of hash sent
   - HTTPS for all API communications

3. **Storage Security**:
   - Fernet symmetric encryption
   - Encrypted history logs
   - Secure key management

4. **Application Security**:
   - Input validation
   - Error handling
   - Secure defaults

## Differentiation

- **Security**: Encrypts password logs to ensure sensitive information is not stored in plain text.
- **Comprehensive**: Combines password checking, generation, and strength analysis in one tool.
- **User-Friendly**: Provides command-line interface, GUI, and an interactive Streamlit dashboard
- **Analytics**: Includes data visualization and security trends through the Streamlit interface
- **Real-Time Feedback**: Offers immediate feedback on password strength and breach status.

## Conclusion

The Password Checker & Generator is a robust tool designed to enhance password security by identifying compromised passwords, generating strong passwords, and providing detailed strength analysis. Its secure logging mechanism and user-friendly interface make it a valuable tool for anyone concerned about password security.
