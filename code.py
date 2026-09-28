import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    status TEXT DEFAULT 'Available'
)
""")

conn.commit()


# Show all books
def refresh_books():
    listbox.delete(0, tk.END)

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    for book in books:
        text = f"{book[0]} | {book[1]} | {book[2]} | {book[3]}"
        listbox.insert(tk.END, text)


# Add a new book
def add_book():
    title = title_entry.get()
    author = author_entry.get()

    if title == "" or author == "":
        messagebox.showwarning(
            "Warning",
            "Please enter book title and author."
        )
        return

    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )

    conn.commit()

    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)

    refresh_books()

    messagebox.showinfo(
        "Success",
        "Book added successfully."
    )


# Search for a book
def search_book():
    search = search_entry.get()

    listbox.delete(0, tk.END)

    cursor.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        ('%' + search + '%', '%' + search + '%')
    )

    books = cursor.fetchall()

    for book in books:
        text = f"{book[0]} | {book[1]} | {book[2]} | {book[3]}"
        listbox.insert(tk.END, text)


# Issue a book
def issue_book():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book."
        )
        return

    book_text = listbox.get(selected[0])
    book_id = book_text.split("|")[0].strip()

    cursor.execute(
        "SELECT status FROM books WHERE id = ?",
        (book_id,)
    )

    result = cursor.fetchone()

    if result is None:
        messagebox.showerror(
            "Error",
            "Book not found."
        )
        return

    if result[0] == "Issued":
        messagebox.showwarning(
            "Warning",
            "This book is already issued."
        )
        return

    cursor.execute(
        "UPDATE books SET status = ? WHERE id = ?",
        ("Issued", book_id)
    )

    conn.commit()

    refresh_books()

    messagebox.showinfo(
        "Success",
        "Book issued successfully."
    )


# Return a book
def return_book():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book."
        )
        return

    book_text = listbox.get(selected[0])
    book_id = book_text.split("|")[0].strip()

    cursor.execute(
        "SELECT status FROM books WHERE id = ?",
        (book_id,)
    )

    result = cursor.fetchone()

    if result is None:
        messagebox.showerror(
            "Error",
            "Book not found."
        )
        return

    if result[0] == "Available":
        messagebox.showwarning(
            "Warning",
            "This book is already available."
        )
        return

    cursor.execute(
        "UPDATE books SET status = ? WHERE id = ?",
        ("Available", book_id)
    )

    conn.commit()

    refresh_books()

    messagebox.showinfo(
        "Success",
        "Book returned successfully."
    )


# Delete a book
def delete_book():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a book."
        )
        return

    book_text = listbox.get(selected[0])
    book_id = book_text.split("|")[0].strip()

    answer = messagebox.askyesno(
        "Delete Book",
        "Are you sure you want to delete this book?"
    )

    if answer:
        cursor.execute(
            "DELETE FROM books WHERE id = ?",
            (book_id,)
        )

        conn.commit()

        refresh_books()

        messagebox.showinfo(
            "Success",
            "Book deleted."
        )


# ---------------- GUI ----------------

root = tk.Tk()
root.title("Mini Library Management System")
root.geometry("1000x800")


# Heading
heading = tk.Label(
    root,
    text="LIBRARY MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)
heading.pack(pady=15)


# Add book section
add_frame = tk.Frame(root)
add_frame.pack(pady=5)

tk.Label(
    add_frame,
    text="Book Title:"
).grid(row=0, column=0, padx=5)

title_entry = tk.Entry(
    add_frame,
    width=25
)
title_entry.grid(row=0, column=1, padx=5)

tk.Label(
    add_frame,
    text="Author:"
).grid(row=0, column=2, padx=5)

author_entry = tk.Entry(
    add_frame,
    width=20
)
author_entry.grid(row=0, column=3, padx=5)

add_button = tk.Button(
    add_frame,
    text="Add Book",
    command=add_book
)
add_button.grid(row=0, column=4, padx=10)


# Search section
search_frame = tk.Frame(root)
search_frame.pack(pady=15)

tk.Label(
    search_frame,
    text="Search:"
).pack(side=tk.LEFT)

search_entry = tk.Entry(
    search_frame,
    width=35
)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(
    search_frame,
    text="Search",
    command=search_book
)
search_button.pack(side=tk.LEFT, padx=5)

show_button = tk.Button(
    search_frame,
    text="Show All",
    command=refresh_books
)
show_button.pack(side=tk.LEFT, padx=5)


# Book list section
list_frame = tk.Frame(root)
list_frame.pack(pady=5)

listbox = tk.Listbox(
    list_frame,
    width=90,
    height=15
)
listbox.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(
    list_frame,
    command=listbox.yview
)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(
    yscrollcommand=scrollbar.set
)


# Buttons section
button_frame = tk.Frame(root)
button_frame.pack(pady=15)

issue_button = tk.Button(
    button_frame,
    text="Issue Book",
    width=15,
    command=issue_book
)
issue_button.grid(row=0, column=0, padx=5)

return_button = tk.Button(
    button_frame,
    text="Return Book",
    width=15,
    command=return_book
)
return_button.grid(row=0, column=1, padx=5)

delete_button = tk.Button(
    button_frame,
    text="Delete Book",
    width=15,
    command=delete_book
)
delete_button.grid(row=0, column=2, padx=5)


# Display books when program starts
refresh_books()


# Run application
root.mainloop()


# Close database connection
conn.close()