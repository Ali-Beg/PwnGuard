import tkinter as tk
from tkinter import messagebox, ttk
from check_my_passwoed import pawned_api_check, generate_strong_password, check_password_strength

class PasswordCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Checker & Generator")
        self.root.geometry("400x300")
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=5)

        # Password Check Frame
        check_frame = ttk.LabelFrame(self.root, text="Check Password", padding=10)
        check_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(check_frame, text="Enter Password:").pack()
        self.entry_password = ttk.Entry(check_frame, show="*")
        self.entry_password.pack()
        ttk.Button(check_frame, text="Check Password", command=self.check_password).pack(pady=5)

        # Password Generator Frame
        gen_frame = ttk.LabelFrame(self.root, text="Generate Password", padding=10)
        gen_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(gen_frame, text="Password Length:").pack()
        self.entry_length = ttk.Entry(gen_frame)
        self.entry_length.insert(0, "12")
        self.entry_length.pack()
        ttk.Button(gen_frame, text="Generate Password", command=self.generate_password).pack(pady=5)

    def check_password(self):
        try:
            password = self.entry_password.get()
            if not password:
                messagebox.showwarning("Warning", "Please enter a password")
                return

            count = pawned_api_check(password)
            strength_score, feedback = check_password_strength(password)
            
            result = []
            if count:
                result.append(f'❌ Password was found {count} times... you should change it!')
            else:
                result.append('✓ Password was NOT found. Carry on!')
            
            result.append(f'\nPassword strength: {strength_score}/5')
            if feedback:
                result.append("\nImprovements needed:")
                result.extend(f"- {suggestion}" for suggestion in feedback)
            
            messagebox.showinfo("Password Check Result", "\n".join(result))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def generate_password(self):
        try:
            length = int(self.entry_length.get())
            if length < 12:
                length = 12
            new_password = generate_strong_password(length)
            count = pawned_api_check(new_password)
            
            result = f"Generated password: {new_password}"
            if count:
                result += "\n\nWarning: This password was found in data breaches!"
            
            messagebox.showinfo("Generated Password", result)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for password length")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = PasswordCheckerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
