import os
import shutil
import requests
from bs4 import BeautifulSoup
from PIL import Image

url = input("URL: ")
# issue_number = 1
image_file_names = []

web_page = requests.get(url)
soup = BeautifulSoup(web_page.text, "html.parser")
img_tags = soup.find_all("img", attrs={"class": "thumbnail"})

image_sources = [image.get("src").strip() for image in img_tags]

# downloads = f"downloads/issue_{issue_number}"
os.makedirs("downloads", exist_ok=True)

for source in image_sources:
    response = requests.get(url + source)
    image_name = os.path.join("downloads", source.split("/")[-1])

    with open(image_name, "wb") as image:
        print(f"Downloading: {image_name}")
        image.write(response.content)
        image_file_names.append(image_name)


images = []
for image in image_file_names:
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    images.append(img)

if images:
    print("Compiling into PDF...")
    images[0].save("output.pdf", save_all=True, append_images=images[1:])

choice = input("Delete images files? (y/n) ")
if choice == "y":
    shutil.rmtree("downloads")
