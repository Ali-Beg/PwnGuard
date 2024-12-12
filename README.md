# PwnGuard - Advanced Password Security Tool  

> **Protect, Generate, and Analyze Your Passwords**  

**[Visit the Live App](https://pwnguard.streamlit.app/)**  

A comprehensive password security tool that checks for compromised passwords using the [Have I Been Pwned](https://haveibeenpwned.com/API/v3#PwnedPasswords) API and includes additional security features.

---

## 🚀 Features  

- **Breach Detection**: Check if your passwords have been compromised in data breaches.  
- **Strong Password Generator**: Create robust passwords with customizable length and criteria.  
- **Password Strength Analysis**: Evaluate your password's strength in real-time.  
- **Password History Tracking**: Log password check results securely.  
- **Interactive Dashboard**: Visualize password analytics and trends with Streamlit.  
- **Colorful Console Output**: Enhanced readability in CLI.  
- **Multiple Operation Modes**:  
  - File-based password checks.  
  - Single password analysis.  
  - Password generation.  
- **Data Visualization**: Gain insights from breach analytics and password trends.  

---

## 🔐 Security Measures  

- **No Plain Text Storage**: Passwords are never stored in plain text.  
- **K-Anonymity Compliance**: Uses HIBP's k-anonymity model, sending only the first 5 characters of the hashed password.  
- **SHA-1 Hashing**: Passwords are hashed before external checks.  
- **Encrypted History Logs**: Password check results are encrypted using Fernet (symmetric encryption).  
- **Memory Safety**: Sensitive data is cleared from memory after use.  
- **HTTPS Only**: Ensures secure API communication.  

---

## 🛠 Requirements  

- Python 3.x  
- Required libraries:  
  ```bash
  pip install -r requirements.txt
  ```  

---

## ⚙️ Setup  

1. **Create a virtual environment**:  
   ```bash
   python -m venv venv
   ```  

2. **Activate the virtual environment**:  
   - **Windows**:  
     ```bash
     venv\Scripts\activate
     ```  
   - **macOS/Linux**:  
     ```bash
     source venv/bin/activate
     ```  

3. **Install dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```  

---

## 📊 Deployment  

### Local Development  

Follow the setup instructions above to run the tool locally.  

### Streamlit Cloud Deployment  

1. Fork this repository.  
2. Visit [Streamlit Cloud](https://streamlit.io/cloud).  
3. Deploy the `streamlit_app.py` file.  
4. Add the following secrets in Streamlit Cloud:  
   ```toml
   [secrets]
   auth_key = "your_encryption_key"
   ```  

---

## 🌐 How to Use  

### **1. Web App**  
Use the [Streamlit Dashboard](https://pwnguard.streamlit.app/) to interact with the tool online.  

### **2. Command Line Interface**  
Run the tool directly:  
```bash
python check_my_password.py
```  

### **3. GUI Mode**  
Launch a graphical interface:  
```bash
python gui.py
```  

### **4. File-based Password Check**  
- Place your passwords in a file (`passwords.txt`), one per line.  
- Run the script and select the appropriate option.  

### **5. Generate Strong Passwords**  
- Select the password generation option in CLI/GUI.  
- Input desired password length (minimum 12 characters).  

### **6. Single Password Check**  
- Input a password directly via CLI or GUI.  

---

## 📋 Password Strength Criteria  

Passwords are evaluated based on:  
- Length (minimum 12 characters).  
- Use of uppercase and lowercase letters.  
- Inclusion of numbers and special characters.  

---

## 📁 History Tracking  

Results are securely logged in `password_history.txt` with:  
- Timestamp.  
- Password strength score.  
- Breach count (if applicable).  

---

## 🔒 Disclaimer  

Use this tool responsibly. Only check passwords that you own or have explicit permission to test.  

