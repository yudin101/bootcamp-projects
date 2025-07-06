import os
import csv
import string
import random

filename = "information.csv"

if not os.path.exists(filename):
    with open(filename, "w", newline="") as file:
        csv.writer(file).writerow(["Username", "Password"])

def random_string_generator(length):
    random_string = ""

    characters = string.ascii_letters + string.digits + string.punctuation

    for _ in range(length):
        random_string += random.choice(characters)

    return random_string


username = input("Enter username: ")

while True:
    password_len = int(input("Enter password length: "))

    if password_len >= 8:
        break

    print("Password length must be at least 8")


with open(filename, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([username, random_string_generator(password_len)])
