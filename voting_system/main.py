import json
import os
import tkinter as tk
from tkinter import scrolledtext

filename = "information.json"


def end():
    with open(filename, "r") as file:
        data = json.load(file)
        first_candidate = data[0]

        for candidate in data:
            if candidate["votes"] > first_candidate["votes"]:
                message_label.config(
                    text=f"Winner: {candidate['name']}\nVotes: {candidate['votes']}",
                    fg="green",
                )
            elif (
                candidate["votes"] == first_candidate["votes"]
                and candidate["name"] != first_candidate["name"]
            ):
                message_label.config(
                    text=f"Tie between: {candidate['name']} and {first_candidate['name']}",
                    fg="yellow",
                )
            else:
                message_label.config(
                    text=f"Winner: {first_candidate['name']}\nVotes: {first_candidate['votes']}",
                    fg="green",
                )


def update_votes(name):
    data = []
    vote_increased = False

    with open(filename, "r") as file:
        data = json.load(file)

        for index, candidate in enumerate(data):
            if candidate["name"] == name:
                data[index]["votes"] += 1
                vote_increased = True
                break

    if vote_increased:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    display_votes()


def display_votes():
    with open(filename, "r") as file:
        data = json.load(file)

        file_contents = ""

        for widget in button_frame.winfo_children():
            widget.destroy()

        for candidate in data:
            file_contents += f"{candidate['name']}, {candidate['votes']}\n"
            tk.Button(
                button_frame,
                text=candidate["name"],
                font=("Arial", 13, "normal"),
                command=lambda name=candidate["name"]: update_votes(name),
            ).pack(side=tk.LEFT)

        tk.Button(
            button_frame, text="End", font=("Arial", 15, "bold"), command=end
        ).pack(side=tk.RIGHT)

        response_box.delete(1.0, tk.END)
        response_box.insert(tk.END, file_contents)


def add_candidate(name):
    if name == "":
        message_label.config(text="Name cannot be empty", fg="red")
        return False

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    name = name.strip()

    for candidate in data:
        if candidate["name"] == name:
            message_label.config(text="Candidate Exists", fg="red")
            return False

    new_candidate = {"name": name, "votes": 0}
    data.append(new_candidate)

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    message_label.config(text="Added", fg="green")
    return True


def click():
    message_label.config(text="")
    wind.update_idletasks()

    candidate_name = candidate_entry.get()

    if add_candidate(candidate_name):
        display_votes()


wind = tk.Tk()
wind.title("Voting System")
wind.geometry("1200x700")

main_frame = tk.Frame(wind)
main_frame.pack(fill=tk.BOTH, expand=True)

entry_frame = tk.LabelFrame(main_frame, padx=10, pady=5)
entry_frame.pack(fill=tk.X)

tk.Label(entry_frame, text="Enter candidate's name: ").pack(side=tk.LEFT)
candidate_entry = tk.Entry(entry_frame, font=("Arial", 15, "normal"))
candidate_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

tk.Button(entry_frame, text="Add", command=click).pack(padx=5, pady=5)

message_label = tk.Label(main_frame, fg="red", font=("Arial", 15, "bold"))
message_label.pack(fill=tk.X)

response_box = scrolledtext.ScrolledText(
    main_frame, wrap=tk.WORD, width=70, height=15, padx=5, pady=5
)
response_box.pack(fill=tk.BOTH, expand=True)

button_frame = tk.Frame(main_frame)
button_frame.pack(fill=tk.X)

if os.path.exists(filename):
    display_votes()

wind.mainloop()
