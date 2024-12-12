import unittest
import string
from check_my_passwoed import check_password_strength, generate_strong_password

class TestPasswordChecker(unittest.TestCase):

    def test_check_password_strength(self):
        password = "StrongPass123!"
        score, feedback = check_password_strength(password)
        self.assertEqual(score, 5)
        self.assertEqual(feedback, [])

    def test_generate_strong_password(self):
        password = generate_strong_password(12)
        self.assertTrue(len(password) >= 12)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

if __name__ == '__main__':
    unittest.main()
