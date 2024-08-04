import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Function to download images from WhatsApp
def download_images_from_whatsapp():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")  # Preserve login session

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Navigate to WhatsApp Web
    driver.get("https://web.whatsapp.com")

    # Specify the directory where you want to save the images
    download_folder = "/Users/ammarmahmood/Downloads"
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

                # Move the downloaded file to the specified directory
                # Assuming the default download location is the system's Downloads folder
                default_download_path = os.path.expanduser("~/Downloads")
                for filename in os.listdir(default_download_path):
                    if filename.endswith(".jpg") or filename.endswith(".png"):
                        os.rename(os.path.join(default_download_path, filename),
                                  os.path.join(download_folder, filename))
                        print(f"Downloaded: {filename}")

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

        # Download the latest image
        download_latest_image()

    finally:
        # Close the browser and quit the driver
        driver.quit()

# Function to upload images to the server
def upload_images_to_server():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")  # Preserve login session

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Navigate to the web application URL
    driver.get("file:///Users/ammarmahmood/Documents/GitHub/camera-frontend/Food-Companion.html")

    # Specify the Downloads folder path
    downloads_folder = "/Users/ammarmahmood/Downloads"

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

    # Wait for a key press before closing the browser and starting a new cycle
    input("Press Enter to start the next cycle...")

    # Close the browser
    driver.quit()

# Function to delete images from the Downloads folder
def delete_downloaded_images():
    download_folder = "/Users/ammarmahmood/Downloads"
    for filename in os.listdir(download_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(download_folder, filename)
            os.remove(file_path)
            print(f"Deleted: {filename}")

# Main execution
if __name__ == "__main__":
    while True:
        download_images_from_whatsapp()
        time.sleep(5)  # Wait for 5 seconds before starting the upload
        upload_images_to_server()
        delete_downloaded_images()
        print("Completed one cycle.")
