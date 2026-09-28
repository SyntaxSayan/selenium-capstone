from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from config.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger
from utilities.screenshot_util import ScreenshotUtil
from utilities.alert_handler import AlertHandler

class BasePage:
    """Base class for all page objects in the Page Object Model (POM)."""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = ConfigReader.get_explicit_wait()
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.alert_handler = AlertHandler(self.driver)

    def navigate_to(self, url):
        """Navigates to specified URL."""
        self.logger.info(f"Navigating to: {url}")
        self.driver.get(url)

    def get_title(self):
        """Returns the current page title."""
        title = self.driver.title
        self.logger.info(f"Page title: '{title}'")
        return title

    def get_current_url(self):
        """Returns current URL."""
        return self.driver.current_url

    def find(self, locator, timeout=None):
        """Finds a single element after waiting for its presence."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator, timeout=None):
        """Finds all matching elements after waiting for at least one."""
        t = timeout if timeout is not None else self.timeout
        try:
            return WebDriverWait(self.driver, t).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []

    def wait_for_visible(self, locator, timeout=None):
        """Waits until element is visible and returns it."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=None):
        """Waits until element is clickable and returns it."""
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator, timeout=None):
        """Clicks an element with fallback to JavaScript click if intercepted."""
        t = timeout if timeout is not None else self.timeout
        element = WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )
        try:
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except (ElementClickInterceptedException, StaleElementReferenceException):
            self.logger.warning(f"Standard click failed for {locator}. Attempting JS click fallback.")
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"JS clicked element: {locator}")

    def send_keys(self, locator, text, clear_first=True, timeout=None):
        """Waits for visibility, optionally clears, and sends keys."""
        element = self.wait_for_visible(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(str(text))
        self.logger.info(f"Entered text '{text}' into element: {locator}")

    def get_text(self, locator, timeout=None):
        """Retrieves inner text of an element."""
        element = self.wait_for_visible(locator, timeout)
        text = element.text.strip()
        self.logger.info(f"Read text '{text}' from element: {locator}")
        return text

    def get_attribute(self, locator, attribute_name, timeout=None):
        """Retrieves attribute value from an element."""
        element = self.find(locator, timeout)
        return element.get_attribute(attribute_name)

    def is_displayed(self, locator, timeout=3):
        """Checks if element is visible on page without throwing exception."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll_into_view(self, locator):
        """Scrolls element into center view."""
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def capture_screenshot(self, step_name):
        """Captures a screenshot with step name."""
        path = ScreenshotUtil.capture_screenshot(self.driver, step_name)
        self.logger.info(f"Screenshot captured for '{step_name}' at: {path}")
        return path
