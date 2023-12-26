from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import os
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from time import sleep
import logging
from extension import proxies
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.CRITICAL)

dir_path = os.path.dirname(os.path.realpath(__file__))
sep = os.sep


def getOptions():
    options = uc.ChromeOptions() 
    # options.add_argument('--ignore-ssl-errors=yes')
    # options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    # options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    options.add_argument("--lang=en-US,en;q=0.9")
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-blink-features=AutomationControlled')
    # options.add_argument("disable-infobars")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    
    return options

def getDriver(proxy :dict = None):
    options = getOptions()
    if proxy:
        print(proxy)
        print(proxy['user'], proxy['pass'], proxy['host'], proxy['port'])
        proxy_extension = proxies(proxy['user'], proxy['pass'], proxy['host'], proxy['port'])
        options.add_argument(f'--load-extension={proxy_extension}')
        
        # options.add_extension(proxy_extension)
    driver = webdriver.Chrome(options=options)
    return driver
