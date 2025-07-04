from tkinter import *
import pytesseract
from PIL import Image
import requests

wind = Tk()
wind.title("Certificate Validation")
wind.geometry("600x600")

file_path_label = Label(wind, text="Enter the file path of your certificate file: ")
file_path_label.pack(pady=10)

file_path_entry = Entry(wind, width=30)
file_path_entry.pack(pady=5)

def get_institution_name(image_path):
    img = Image.open(image_path)
    img = img.convert('L') 
    text = pytesseract.image_to_string(img)

    lines = text.split("\n")
    for line in lines:
        if (
            "university" in line.lower()
            or "college" in line.lower()
            or "institute" in line.lower()
            or "academy" in line.lower()
        ):
            return line.strip()
    return None  


def check_website_exists(url):
    try:
        response = requests.head(url, timeout=5) 
        return 200 <= response.status_code < 400 
    except requests.exceptions.RequestException:
        return False


def verify_online_presence(institution_name):
    cleaned_name = institution_name.replace(" ", "").lower()
    
    potential_domains = [
        f"www.{cleaned_name}.edu",
        f"www.{cleaned_name}.org",
        f"www.{cleaned_name}.com",
        f"www.{cleaned_name}.edu.np", 
    ]

    for domain in potential_domains:
        if check_website_exists(f"http://{domain}") or check_website_exists(f"https://{domain}"):
            return True, domain 
    return False, None 

def validate():
    institution_name = get_institution_name(file_path_entry.get())
    if institution_name:
        print(f"Extracted Institution: {institution_name}")

        extracted_institution_label.config(text=f"Extracted Institution: {institution_name}", fg="green")

        has_online_presence, website = verify_online_presence(institution_name)
        if has_online_presence:
            print(f"Institution has an online presence: {website}")
            online_presence_label.config(text=f"Institution has an online presence: {website}", fg="green")
        else:
            print("Institution does NOT appear to have a direct online presence.")
            online_presence_label.config(text="Institution does NOT appear to have a direct online presence.", fg="red")
    else:
        print("Could not extract institution name.")
        extracted_institution_label.config(text="Could not extract institution name.", fg="red")
        online_presence_label.config(text="")

submit_button = Button(wind, text="Validate", command=validate)
submit_button.pack(pady=10)

extracted_institution_label = Label(wind, text="")
extracted_institution_label.pack(pady=5)

online_presence_label = Label(wind, text="")
online_presence_label.pack(pady=5)

wind.mainloop()
