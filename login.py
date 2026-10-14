import tkinter as tk
from tkinter import messagebox
import database
import ui

def login_screen():
    def login_action():
        user = database.verify_user(username.get(), password.get())
        if user:
            root.destroy()
            ui.main_app(user)
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    def register_action():
        if database.create_user(username.get(), password.get()):
            messagebox.showinfo("Success", "Account created! You can log in now.")
        else:
            messagebox.showerror("Error", "Username already exists!")

    root = tk.Tk()
    root.title("Expense Tracker Login")
    root.geometry("750x650")
    root.resizable(False, False)

    tk.Label(root, text="Login", font=("Arial", 28, "bold")).pack(pady=20)
    tk.Label(root, text="Username").pack()
    username = tk.Entry(root)
    username.pack()

    tk.Label(root, text="Password").pack()
    password = tk.Entry(root, show="*")
    password.pack()

    tk.Button(root, text="Login", width=22, command=login_action).pack(pady=20)
    tk.Button(root, text="Register", width=22, command=register_action).pack()

    root.mainloop()
