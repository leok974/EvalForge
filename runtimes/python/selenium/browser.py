from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service

def build_driver():
    """
    Builds a canonical headless Chrome driver for EvalForge quests.
    Ensures deterministic resizing and standard CI-safe arguments.
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1024")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Avoid "Chrome is being controlled by automated test software" infobar
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)
    
    # Set standard timeout
    driver.implicitly_wait(5)
    
    return driver
