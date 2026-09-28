from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, NoSuchElementException
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("AlertHandler")

class AlertHandler:
    """Handles both JavaScript native alerts and DOM-based popups/modal dialogs."""

    def __init__(self, driver):
        self.driver = driver

    # ---------------- NATIVE JAVASCRIPT ALERTS ---------------- #

    def is_js_alert_present(self, timeout=3):
        """Checks if a native JavaScript alert is present within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            return True
        except (TimeoutException, NoAlertPresentException):
            return False

    def accept_js_alert(self, timeout=3):
        """Waits for and accepts a native JavaScript alert."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            logger.info(f"Accepted JavaScript alert with text: '{text}'")
            return text
        except (TimeoutException, NoAlertPresentException):
            logger.debug("No JavaScript alert present to accept.")
            return None

    def dismiss_js_alert(self, timeout=3):
        """Waits for and dismisses a native JavaScript alert."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.dismiss()
            logger.info(f"Dismissed JavaScript alert with text: '{text}'")
            return text
        except (TimeoutException, NoAlertPresentException):
            logger.debug("No JavaScript alert present to dismiss.")
            return None

    def get_js_alert_text(self, timeout=3):
        """Gets text of a native JavaScript alert without closing it."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            return alert.text
        except (TimeoutException, NoAlertPresentException):
            return None

    # ---------------- DOM / BOOTSTRAP MODALS & NOTIFICATION POPUPS ---------------- #

    def dismiss_bootstrap_alert(self, timeout=5):
        """Dismisses on-page bootstrap alert notification (e.g. .alert .close)."""
        try:
            close_btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".alert button.close, .alert .close"))
            )
            close_btn.click()
            logger.info("Dismissed bootstrap banner alert.")
            return True
        except (TimeoutException, NoSuchElementException):
            logger.debug("No bootstrap alert close button found.")
            return False

    def close_modal_if_present(self, modal_close_locator=(By.CSS_SELECTOR, ".modal .close, button[data-dismiss='modal']"), timeout=3):
        """Dismisses a modal popup if one appears on screen."""
        try:
            close_btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(modal_close_locator)
            )
            close_btn.click()
            logger.info("Dismissed modal popup.")
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def handle_any_alert_or_popup(self, timeout=3):
        """Smart method that attempts to dismiss native JS alert, modal, or banner popup."""
        if self.is_js_alert_present(timeout=1):
            return self.accept_js_alert(timeout=1)
        if self.close_modal_if_present(timeout=1):
            return "Modal dismissed"
        if self.dismiss_bootstrap_alert(timeout=1):
            return "Banner dismissed"
        return None
