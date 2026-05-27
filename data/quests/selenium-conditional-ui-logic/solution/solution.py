from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

driver.get("http://mock-cms:8765/modals?show_modal=true")

try:
    modal_cancel = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='modal-cancel']"))
    )
    modal_cancel.click()
    
    WebDriverWait(driver, 2).until(
        EC.invisibility_of_element((By.CSS_SELECTOR, "[data-testid='override-modal']"))
    )
except TimeoutException:
    pass

driver.find_element(By.CSS_SELECTOR, "[data-testid='trigger-override']").click()
print("DEFENSE_ACTIVE")
driver.quit()
