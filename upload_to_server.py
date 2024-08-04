import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")  # Preserve login session

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the web application URL
driver.get("file:///Users/ammarmahmood/Documents/GitHub/camera-frontend/Food-Companion.html")

# Specify the Downloads folder path
downloads_folder = os.path.expanduser("~/Downloads")

# Find the first image file in the Downloads folder
image_files = [f for f in os.listdir(downloads_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
if not image_files:
    print("No image files found in the Downloads folder.")
else:
    # Get the path of the first image file
    first_image_path = os.path.join(downloads_folder, image_files[0])

    # Locate the "Choose File" button and upload the image
    choose_file_button = driver.find_element(By.XPATH, "//input[@type='file']")
    choose_file_button.send_keys(first_image_path)

    print(f"Uploaded: {first_image_path}")

# Wait for the user to press Enter before closing the browser
input("Press Enter to close the browser and end the script...")

# Close the browser
driver.quit()
