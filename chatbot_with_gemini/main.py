import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import requests
import json


def generate_text_with_gemini(prompt, model_name="gemini-2.0-flash", api_key=""):
    chat_history = []
    chat_history.append({"role": "user", "parts": [{"text": prompt}]})

    payload = {"contents": chat_history}

    # Construct the API URL
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        result = response.json()

        if (
            result.get("candidates")
            and len(result["candidates"]) > 0
            and result["candidates"][0].get("content")
            and result["candidates"][0]["content"].get("parts")
            and len(result["candidates"][0]["content"]["parts"]) > 0
        ):
            generated_text = result["candidates"][0]["content"]["parts"][0].get("text")
            return generated_text
        else:
            return f"Error: Unexpected response structure or no content from Gemini API. Response: {result}"

    except requests.exceptions.RequestException as e:
        return f"Error making API request: {e}"
    except json.JSONDecodeError:
        return f"Error decoding JSON response: {response.text}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def click():
    my_api_key = "" # Put your API Key

    user_prompt = prompt_entry.get()

    if user_prompt == "":
        response_box.delete(1.0, tk.END)
        response_box.insert(tk.END, "Please enter a prompt!")
        return

    response_box.delete(1.0, tk.END)
    response_box.insert(tk.END, "Thinking...")
    wind.update_idletasks()

    response_text = generate_text_with_gemini(user_prompt, api_key=my_api_key)

    response_box.delete(1.0, tk.END)
    response_box.insert(tk.END, response_text)

wind = tk.Tk()
wind.geometry("1000x700")
wind.title("Chatbot with Gemini")

main_frame = ttk.Frame(wind, padding="10 10 10 10")
main_frame.pack(fill=tk.BOTH, expand=True)

prompt_frame = ttk.LabelFrame(main_frame)
prompt_frame.pack(fill=tk.X)

ttk.Label(prompt_frame, text="Enter your prompt: ").pack(side=tk.LEFT, padx=5, pady=5)

prompt_entry = tk.Entry(prompt_frame, width=30)
prompt_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

submit_button = tk.Button(prompt_frame, text="Submit", command=click)
submit_button.pack(pady=5, padx=5)

response_box = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=15, padx=5, pady=5)
response_box.pack(fill=tk.BOTH, expand=True)
response_box.insert(tk.END, "Ask me anything!")

wind.mainloop()
