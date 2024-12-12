import unittest
import string
import os
from check_my_passwoed import (
    check_password_strength,
    generate_strong_password,
    pawned_api_check,
    encrypt_message,
    decrypt_message
)

class TestPasswordSecurity(unittest.TestCase):
    def test_password_strength(self):
        # Test weak password
        score, feedback = check_password_strength("password123")
        self.assertEqual(score, 3)
        self.assertTrue(len(feedback) > 0)

        # Test strong password
        score, feedback = check_password_strength("StrongP@ssw0rd123!")
        self.assertEqual(score, 5)
        self.assertEqual(len(feedback), 0)

    def test_password_generator(self):
        # Test password length
        password = generate_strong_password(16)
        self.assertEqual(len(password), 16)

        # Test password complexity
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_api_connection(self):
        # Test API with known compromised password
        count = pawned_api_check("password123")
        self.assertTrue(count > 0)

        # Test API with complex password
        count = pawned_api_check(generate_strong_password(32))
        self.assertEqual(count, 0)

    def test_encryption(self):
        test_message = "Test message 123"
        # Test encryption
        encrypted = encrypt_message(test_message)
        self.assertIsNotNone(encrypted)
        
        # Test decryption
        decrypted = decrypt_message(encrypted)
        self.assertEqual(decrypted, test_message)

def run_system_test():
    """Test the entire system workflow"""
    try:
        # Test command-line interface
        exit_code = os.system('python check_my_passwoed.py')
        print(f"\nCLI Test {'passed' if exit_code == 0 else 'failed'}")

        # Test GUI
        exit_code = os.system('python gui.py')
        print(f"GUI Test {'passed' if exit_code == 0 else 'failed'}")

        # Test Streamlit app
        exit_code = os.system('streamlit run streamlit_app.py --headless')
        print(f"Streamlit Test {'passed' if exit_code == 0 else 'failed'}")

    except Exception as e:
        print(f"System test failed: {str(e)}")

if __name__ == '__main__':
    # Run unit tests
    print("Running unit tests...")
    unittest.main(verbosity=2, exit=False)

    # Run system tests
    print("\nRunning system tests...")
    run_system_test()
