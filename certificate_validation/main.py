from tkinter import *
from tkinter import filedialog
import pytesseract
from PIL import Image
import requests

wind = Tk()
wind.title("Certificate Validation")
wind.geometry("600x600")

def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select Certificate Image",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All Files", "*.*"),
        ],
    )
    if file_path:
        file_path_label.config(text=f"Checking validity of : {file_path}")

        error_label.config(text="")
        extracted_institution_label.config(text="")
        online_presence_label.config(text="")

        wind.update_idletasks()

        return file_path


def get_institution_name(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert("L")
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
    except Exception as e:
        error_label.config(text=e)
        wind.update_idletasks()


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
        if check_website_exists(f"http://{domain}") or check_website_exists(
            f"https://{domain}"
        ):
            return True, domain
    return False, None


def validate():
    institution_name = get_institution_name(open_file_dialog())
    if institution_name:
        extracted_institution_label.config(
            text=f"Extracted Institution: {institution_name}", fg="green"
        )
        wind.update_idletasks()

        has_online_presence, website = verify_online_presence(institution_name)
        if has_online_presence:
            online_presence_label.config(
                text=f"Institution has an online presence: {website}", fg="green"
            )
            wind.update_idletasks()
        else:
            online_presence_label.config(
                text="Institution does NOT appear to have a direct online presence.",
                fg="red",
            )
            wind.update_idletasks()
    else:
        extracted_institution_label.config(
            text="Could not extract institution name.", fg="red"
        )
        online_presence_label.config(text="")
        wind.update_idletasks()


validate_button = Button(wind, text="Open File", command=validate)
validate_button.pack(pady=10)

file_path_label = Label(wind, text="")
file_path_label.pack(pady=10)

error_label = Label(wind, text="", fg="red")
error_label.pack(pady=10)

extracted_institution_label = Label(wind, text="")
extracted_institution_label.pack(pady=5)

online_presence_label = Label(wind, text="")
online_presence_label.pack(pady=5)

wind.mainloop()
