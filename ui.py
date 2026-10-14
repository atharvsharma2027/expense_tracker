import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import database
import login

def main_app(user_id):
    def add_expense():
        date = date_entry.get() or datetime.now().strftime("%Y-%m-%d")
        category = category_entry.get()
        amount = amount_entry.get()
        desc = desc_entry.get()

        if not category or not amount:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        conn = database.connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses(user_id, date, category, amount, description) VALUES(?, ?, ?, ?, ?)",
                    (user_id, date, category, amount, desc))
        conn.commit()
        conn.close()
        load_data()
        clear_entries()
        messagebox.showinfo("Success", "Expense added!")

    def load_data():
        for i in tree.get_children():
            tree.delete(i)

        conn = database.connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, date, category, amount, description FROM expenses WHERE user_id=? ORDER BY date DESC", (user_id,))
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)
        conn.close()

    def delete_expense():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an expense to delete.")
            return

        exp_id = tree.item(selected[0])['values'][0]
        conn = database.connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id=? AND user_id=?", (exp_id, user_id))
        conn.commit()
        conn.close()
        load_data()
        messagebox.showinfo("Deleted", "Expense deleted successfully.")

    def export_csv():
        conn = database.connect_db()
        cur = conn.cursor()
        cur.execute("SELECT date, category, amount, description FROM expenses WHERE user_id=?", (user_id,))
        data = cur.fetchall()
        conn.close()

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Amount", "Description"])
            writer.writerows(data)
        messagebox.showinfo("Exported", "Data exported successfully!")

    def show_chart():
        conn = database.connect_db()
        cur = conn.cursor()
        cur.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id=? GROUP BY category", (user_id,))
        data = cur.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("Info", "No expenses to show.")
            return

        categories = [x[0] for x in data]
        totals = [x[1] for x in data]

        plt.bar(categories, totals)
        plt.title("Spending Summary by Category")
        plt.xlabel("Category")
        plt.ylabel("Total Amount (₹)")
        plt.show()

    def clear_entries():
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("800x500")
    root.resizable(False, False)

    tk.Label(root, text="Expense Tracker", font=("Arial", 18, "bold")).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=5)

    tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
    date_entry = tk.Entry(frame, width=15)
    date_entry.grid(row=0, column=1, padx=5)

    tk.Label(frame, text="Category:").grid(row=0, column=2, padx=5)
    category_entry = tk.Entry(frame, width=15)
    category_entry.grid(row=0, column=3, padx=5)

    tk.Label(frame, text="Amount:").grid(row=0, column=4, padx=5)
    amount_entry = tk.Entry(frame, width=10)
    amount_entry.grid(row=0, column=5, padx=5)

    tk.Label(frame, text="Description:").grid(row=0, column=6, padx=5)
    desc_entry = tk.Entry(frame, width=20)
    desc_entry.grid(row=0, column=7, padx=5)

    tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)

    columns = ("ID", "Date", "Category", "Amount", "Description")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Delete", command=delete_expense).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Export CSV", command=export_csv).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Show Chart", command=show_chart).grid(row=0, column=2, padx=10)
    tk.Button(btn_frame, text="Exit", command=root.destroy).grid(row=0, column=3, padx=10)
    tk.Button(btn_frame, text="Back", command=login.login_screen).grid(row=0, column=4, padx=10)

    load_data()
    root.mainloop()
