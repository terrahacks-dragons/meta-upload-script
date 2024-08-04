import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=chrome-data")  # Preserve login session

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to WhatsApp Web
driver.get("https://web.whatsapp.com")

# Specify the directory where you want to save the images
download_folder = os.path.expanduser("/Users/ammarmahmood/Downloads")
os.makedirs(download_folder, exist_ok=True)

def wait_for_login():
    """Wait for the user to log in by checking for the presence of the chat list."""
    print("Waiting for WhatsApp Web login...")
    while True:
        try:
            # Attempt to find the chat list element to confirm login
            chat_list = driver.find_element(By.XPATH, "//div[@role='grid']")
            if chat_list.is_displayed():
                print("Logged in successfully!")
                break
        except NoSuchElementException:
            pass
        time.sleep(5)  # Check every 5 seconds

def open_first_chat():
    """Open the first chat in the chat list."""
    try:
        first_chat = driver.find_element(By.XPATH, "//div[@role='row']")
        first_chat.click()
        time.sleep(2)  # Allow time for the chat to load
    except NoSuchElementException:
        print("Could not find the first chat. Make sure you are logged in.")

def download_latest_image():
    """Download the latest image from the opened chat."""
    try:
        images = driver.find_elements(By.XPATH, "//img[contains(@src, 'blob:')]")
        if images:
            latest_image = images[-1]  # Assuming the last image in the list is the latest
            latest_image.click()
            time.sleep(2)  # Allow image to load

            # Find the download button and click it
            download_button = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label='Download']")
            download_button.click()
            time.sleep(3)  # Allow time for the download to start

            # Close the image preview
            close_button = driver.find_element(By.XPATH, "//span[@data-icon='x-viewer']")
            close_button.click()
            time.sleep(1)  # Allow UI to reset
        else:
            print("No images found in the chat.")
    except NoSuchElementException:
        print("Error downloading the latest image. Ensure that the chat is open and contains images.")

try:
    # Wait for the user to log in
    wait_for_login()

    # Open the first chat
    open_first_chat()
    download_latest_image()
    time.sleep(4)  
	
except KeyboardInterrupt :
    print("Script stopped by user.")
    
finally:
    driver.quit()

