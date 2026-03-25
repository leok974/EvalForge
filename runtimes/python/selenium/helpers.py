"""
EvalForge Selenium Quest Helpers
Thin wrappers around Selenium calls that emit step log events automatically.
Quest code can use these instead of raw Selenium calls to get a free, ordered trace.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .step_logger import SeleniumStepLogger


def open_page(driver: WebDriver, url: str, logger: SeleniumStepLogger, label: str = None) -> None:
    """Navigate to a URL and log the action."""
    label = label or f"Open page: {url}"
    logger.step("navigate", label, url=url)
    try:
        driver.get(url)
        logger.pass_step()
    except Exception as e:
        logger.fail_step(str(e))
        raise


def find(driver: WebDriver, selector: str, logger: SeleniumStepLogger, label: str = None, by=By.CSS_SELECTOR):
    """Locate an element and log the action."""
    label = label or f"Find element: {selector}"
    logger.step("find", label, selector=selector, url=_url(driver))
    try:
        el = driver.find_element(by, selector)
        logger.pass_step()
        return el
    except Exception as e:
        logger.fail_step(str(e))
        raise


def click(driver: WebDriver, selector: str, logger: SeleniumStepLogger, label: str = None, by=By.CSS_SELECTOR):
    """Find and click an element, logging the action."""
    label = label or f"Click: {selector}"
    logger.step("click", label, selector=selector, url=_url(driver))
    try:
        el = driver.find_element(by, selector)
        el.click()
        logger.pass_step()
        return el
    except Exception as e:
        logger.fail_step(str(e))
        raise


def type_text(driver: WebDriver, selector: str, text: str, logger: SeleniumStepLogger, label: str = None, by=By.CSS_SELECTOR):
    """Find an element, clear it, type text, and log the action."""
    label = label or f"Type into: {selector}"
    logger.step("type", label, selector=selector, url=_url(driver))
    try:
        el = driver.find_element(by, selector)
        el.clear()
        el.send_keys(text)
        logger.pass_step()
        return el
    except Exception as e:
        logger.fail_step(str(e))
        raise


def wait_for(driver: WebDriver, condition, logger: SeleniumStepLogger, label: str = None, timeout: float = 10.0):
    """Wait for an expected condition and log the action."""
    label = label or "Wait for condition"
    logger.step("wait", label, url=_url(driver))
    try:
        result = WebDriverWait(driver, timeout).until(condition)
        logger.pass_step()
        return result
    except Exception as e:
        logger.fail_step(str(e)[:200])
        raise


def assert_text(driver: WebDriver, selector: str, expected: str, logger: SeleniumStepLogger, label: str = None, by=By.CSS_SELECTOR):
    """Find an element and assert its text matches expected."""
    label = label or f"Assert text in: {selector}"
    logger.step("assert", label, selector=selector, url=_url(driver))
    try:
        el = driver.find_element(by, selector)
        actual = el.text.strip()
        assert actual == expected, f"Expected '{expected}', got '{actual}'"
        logger.pass_step()
        return actual
    except Exception as e:
        logger.fail_step(str(e))
        raise


# --- internal helpers ---

def _url(driver: WebDriver) -> str:
    try:
        return driver.current_url
    except Exception:
        return ""
