import psutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

CHANNEL_ID = "UC1sWMZGSOen46Lmp8D8CEAQ"
UPLOAD_URL = f"https://studio.youtube.com/channel/{CHANNEL_ID}/videos/upload?d=ud"

CHROME_DRIVER_PATH = r'C:\Users\Shai grossman\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
USER_DATA_PATH = r'C:\Users\Shai grossman\AppData\Local\Google\Chrome\User Data'


def uploadVideo(EXPORTED_VIDEO_PATH, FILE_NAME, FILE_EXTENSION):
    print(EXPORTED_VIDEO_PATH)
    print(FILE_NAME)
    print(FILE_EXTENSION)

    # close all chrome instances before launching selenium
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in ['chrome.exe', 'chromedriver.exe']:
            proc.kill()

    options = Options()
    options.add_argument(fr"--user-data-dir={USER_DATA_PATH}")
    options.add_argument("--profile-directory=Default")

    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
    driver.get(UPLOAD_URL)

    driver.implicitly_wait(10)

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")

    # Send the file path to the file input element
    file_input.send_keys(EXPORTED_VIDEO_PATH + FILE_NAME + FILE_EXTENSION)

    radio_button = driver.find_element(By.XPATH, "//tp-yt-paper-radio-button[@name='VIDEO_MADE_FOR_KIDS_NOT_MFK']")
    radio_button.click()

    button = driver.find_element(By.XPATH,
                                 "//button[@class='ytcp-button-shape-impl ytcp-button-shape-impl--filled ytcp-button-shape-impl--mono ytcp-button-shape-impl--size-m' and @aria-label='הבא']")
    button.click()

    button = driver.find_element(By.XPATH,
                                 "//button[@class='ytcp-button-shape-impl ytcp-button-shape-impl--filled ytcp-button-shape-impl--mono ytcp-button-shape-impl--size-m' and @aria-label='הבא']")
    button.click()

    button = driver.find_element(By.XPATH,
                                 "//button[@class='ytcp-button-shape-impl ytcp-button-shape-impl--filled ytcp-button-shape-impl--mono ytcp-button-shape-impl--size-m' and @aria-label='הבא']")
    button.click()

    radio_button = driver.find_element(By.XPATH, "//tp-yt-paper-radio-button[@id='private-radio-button']")
    radio_button.click()

    button = driver.find_element(By.XPATH,
                                 "//button[@class='ytcp-button-shape-impl ytcp-button-shape-impl--filled ytcp-button-shape-impl--mono ytcp-button-shape-impl--size-m' and @aria-label='שמירה']")
    button.click()

    input("press enter to close the program")
