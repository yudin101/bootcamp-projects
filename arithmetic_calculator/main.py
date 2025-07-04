from tkinter import Button, Tk, Label, filedialog
import pytesseract
from PIL import Image
import re
import os

wind = Tk()
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
        file_path_label.config(text=f"Calculating: {file_path}")

        extracted_text_label.config(text="")
        result_label.config(text="")
        error_label.config(text="")

        wind.update_idletasks()

        return file_path
    else:
        return "No file provided"


# --- Arithmetic Solver Logic ---
def solve_expression(expression_str):
    if not expression_str:
        return "Error: Empty expression"

    try:
        cleaned_expression = expression_str.replace(" ", "")
        
        # A very basic check to ensure it mostly contains numbers, operators, parentheses
        # This regex allows digits, whitespace, basic arithmetic operators, parentheses, and dots (for decimals)
        if not re.fullmatch(r"[\d\s\+\-\*\/\(\)\.]+", cleaned_expression):
            return "Error: Invalid characters in expression."

        # Evaluate the expression
        result = eval(cleaned_expression)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero!"
    except SyntaxError:
        return "Error: Invalid expression syntax."
    except Exception as e:
        return f"Error: {e}"

# --- Image Processing and OCR ---
def extract_text_from_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'")
        return None

    try:
        img = Image.open(image_path)
        img = img.convert('L') # Convert to grayscale
        
        text = pytesseract.image_to_string(img)
        return text.strip()
    except pytesseract.TesseractNotFoundError:
        print("Error: Tesseract OCR engine not found. Please install it.")
        return None
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# --- Main Execution Block ---
def calculate():
    image_file_path = open_file_dialog()
    
    print(f"Attempting to extract text from: {image_file_path}")

    extracted_text = extract_text_from_image(image_file_path)

    if extracted_text is None:
        print("Failed to extract text due to an error.")
        error_label.config(text="Failed to extract text due to an error.")
        wind.update_idletasks()
    elif not extracted_text:
        print("No text found in the image.")
        error_label.config(text="No text found in the image.")
        wind.update_idletasks()
    else:
        print(f"\nExtracted Expression: '{extracted_text}'")
        extracted_text_label.config(text=f"\nExtracted Expression: '{extracted_text}'")
        wind.update_idletasks()
        
        calculation_result = solve_expression(extracted_text)

        if calculation_result[:6] == "Error:":
            error_label.config(text=calculation_result)
            wind.update_idletasks()
            return

        print(f"Calculated Result: {calculation_result}")

        result_label.config(text=f"Calculated Result: {calculation_result}")
        wind.update_idletasks()

open_file_button = Button(wind, text="Open File", command=calculate)
open_file_button.pack(pady=10)

file_path_label = Label(wind, text="")
file_path_label.pack(pady=10)

extracted_text_label = Label(wind, text="")
extracted_text_label.pack(pady=10)

result_label = Label(wind, text="", fg="green")
result_label.pack(pady=10)

error_label = Label(wind, text="", fg="red")
error_label.pack(pady=10)

wind.mainloop()
