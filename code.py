import itertools
import tkinter as tk
from tkinter import ttk, messagebox

#The task was implemented as a "simple password checker" to check the ease or availability of the password
def pass_file(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []
    except UnicodeDecodeError:
        return []

def dictionary_attack(dictionary_file, password_2check):
    passwords = pass_file(dictionary_file)
    return password_2check in passwords

def brute_force_attack(password_2check):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for attempt in itertools.product(chars, repeat=len(password_2check)):
        password = ''.join(attempt)
        if password == password_2check:
            return True
    return False

def check_password():
    password = entry_password.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    result_label.config(text="Checking...", foreground="blue")
    root.update()
    
    if dictionary_attack('hashmob.txt', password):
        result_label.config(text="[✅] Password found --> Dictionary Attack", foreground="green")
    elif brute_force_attack(password):
        result_label.config(text="[✅] Password found --> Brute Force Attack", foreground="orange")
    else:
        result_label.config(text="[❌] Password not found", foreground="red")

root = tk.Tk()
root.title("Password Security Checker")
root.geometry("400x250")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

label = ttk.Label(frame, text="Enter Password:")
label.pack()

entry_password = ttk.Entry(frame, width=30, show="*")
entry_password.pack(pady=5)

btn_check = ttk.Button(frame, text="Check Password", command=check_password)
btn_check.pack(pady=10)

result_label = ttk.Label(frame, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
