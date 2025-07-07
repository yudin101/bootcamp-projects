import os
import csv
import string
import random
import tkinter as tk
from tkinter import scrolledtext

filename = "information.csv"
file_contents = ""

"""
    Checking if information.csv exists 
    Adding the first row if it does not
"""
if not os.path.exists(filename):
    with open(filename, "w", newline="") as file:
        csv.writer(file).writerow(["Username", "Password"])

def read_file():
    """
        Reading the contents of information.csv
        Adding the contents in file_contents
        Updating the GUI with new contents
    """

    global file_contents
    file_contents = ""

    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            file_contents += f"{row[0]}, {row[1]}\n"

    response_box.delete(1.0, tk.END)
    response_box.insert(tk.END, file_contents)


def random_string_generator(length):
    random_string = ""

    characters = string.ascii_letters + string.digits + string.punctuation

    for _ in range(length):
        random_string += random.choice(characters)

    return random_string


def click():
    message_label.config(text="")
    wind.update_idletasks()

    username = username_entry.get()

    if not username:
        message_label.config(text="Username cannot be empty")
        return

    if password_entry.get() == "":
        message_label.config(text="Password length cannot be empty")
        return

    try:
        password_len = int(password_entry.get())
    except ValueError:
        message_label.config(text="Password length must be a valid integer")
        return

    if password_len < 8:
        message_label.config(text="Password length must be at least 8")
        return

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, random_string_generator(password_len)])

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    message_label.config(text="Added!", fg="Green")

    read_file()


wind = tk.Tk()
wind.title("Password Manager")
wind.geometry("1200x700")

main_frame = tk.Frame(wind, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

entry_frame = tk.LabelFrame(main_frame, padx=10, pady=10)
entry_frame.pack(fill=tk.X)

tk.Label(entry_frame, text="Enter username: ").pack(side=tk.LEFT, padx=5, pady=5)
username_entry = tk.Entry(entry_frame)
username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

tk.Label(entry_frame, text="Enter password length: ").pack(side=tk.LEFT, padx=5, pady=5)
password_entry = tk.Entry(entry_frame)
password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

tk.Button(entry_frame, text="Add", command=click).pack(padx=5, pady=5)

message_label = tk.Label(main_frame, fg="red", font=("Arial", 15, "bold"))
message_label.pack(fill=tk.X)

response_box = scrolledtext.ScrolledText(
    main_frame, wrap=tk.WORD, width=70, height=15, padx=5, pady=5
)
response_box.pack(fill=tk.BOTH, expand=True)
read_file()

wind.mainloop()
