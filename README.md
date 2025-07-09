# Bootcamp Projects

## [Certificate Validation](https://github.com/yudin101/bootcamp-projects/tree/main/certificate_validation)
### How it works?
- Upload a picture of a certificate
- Finds the name of the institution
- Searches for any online presence of the institution
- If found, certificate valid
- Else, invalid

### Packages Used
- tkinter
- pytesseract
- pillow
- requests

## [Arithmetic Calculator](https://github.com/yudin101/bootcamp-projects/tree/main/arithmetic_calculator)
### How it works?
- Upload a picture of an arithmetic problem
- Extract the text from the picture
- Calculate it
- Show result

### Packages Used
- tkinter
- pytesseract
- pillow
- re
- os

## [Chatbot with Gemini](https://github.com/yudin101/bootcamp-projects/tree/main/chatbot_with_gemini)
### How it works?
- Enter a prompt
- It is sent to Gemini's API *(get the API Key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey))*
- Receive Gemini's Response

### Packages Used
- tkinter
- requests
- json

## [Password Manager](https://github.com/yudin101/bootcamp-projects/tree/main/password_manager)
### How it works?
- Enter username and password length
- Information gets saved in a CSV file
- Displays the contnets of the CSV file

### Packages Used
- os 
- csv 
- string
- random
- tkinter

## [Finger Detection](https://github.com/yudin101/bootcamp-projects/tree/main/finger_detection)
### How it works?
- Calculates the position of TIP and PIP of the fingers
- If coordinates of TIP is higher than that of PIP, finger count increases
- X coordinate is calculated for thumb and Y coordinate for other fingers

### Packages Used
- opencv
- mediapipe

## [Voting System](https://github.com/yudin101/bootcamp-projects/tree/main/voting_system)
### How it works?
- Enter the candidate's name
- A button with the candidate's name appears at the bottom
- Click that to increase votes
- Information gets saved in a JSON file

### Packages Used
- tkinter
- json

## [Web Scraper](https://github.com/yudin101/bootcamp-projects/tree/main/web_scraper)
### How it works?
- Enter the URL of a website
- Downloads all the images from that website having certain class
- Puts all the images into a PDF

### Pacakges Used
- os
- shutil
- requests
- bs4
- pillow
