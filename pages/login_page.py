from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config_reader import ConfigReader

import time

class LoginPage(BasePage):
    """Page Object for TutorialsNinja Login and Registration Page."""

    LOGIN_URL = "https://tutorialsninja.com/demo/index.php?route=account/login"
    REGISTER_URL = "https://tutorialsninja.com/demo/index.php?route=account/register"

    # Login Locators
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Login']")
    WARNING_ALERT = (By.CSS_SELECTOR, ".alert-danger")
    ACCOUNT_HEADER = (By.XPATH, "//h2[text()='My Account']")
    MY_ACCOUNT_LINK = (By.XPATH, "//span[text()='My Account']")
    LOGOUT_LINK = (By.XPATH, "//a[contains(@href, 'route=account/logout')]")

    # Registration Locators
    FIRSTNAME_INPUT = (By.ID, "input-firstname")
    LASTNAME_INPUT = (By.ID, "input-lastname")
    REG_EMAIL_INPUT = (By.ID, "input-email")
    TELEPHONE_INPUT = (By.ID, "input-telephone")
    REG_PASSWORD_INPUT = (By.ID, "input-password")
    CONFIRM_PASSWORD_INPUT = (By.ID, "input-confirm")
    AGREE_CHECKBOX = (By.NAME, "agree")
    CONTINUE_BUTTON = (By.XPATH, "//input[@value='Continue']")
    SUCCESS_REGISTER_HEADING = (By.XPATH, "//div[@id='content']//h1[text()='Your Account Has Been Created!']")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Navigates directly to the login page."""
        self.navigate_to(self.LOGIN_URL)
        return self

    def login(self, email, password):
        """Fills in credentials and clicks login."""
        self.logger.info(f"Attempting login with email: {email}")
        if not self.is_displayed(self.EMAIL_INPUT, timeout=5):
            self.logger.info("Email input not displayed (possibly already logged in).")
            return self
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def is_logged_in(self):
        """Checks if login was successful (by URL or presence of account elements)."""
        current_url = self.get_current_url()
        if "route=account/account" in current_url or "route=account/success" in current_url:
            return True
        logout_elements = self.find_all(self.LOGOUT_LINK, timeout=2)
        if logout_elements:
            return True
        return self.is_displayed(self.ACCOUNT_HEADER, timeout=2)

    def get_warning_message(self):
        """Gets error banner message text if login failed."""
        if self.is_displayed(self.WARNING_ALERT, timeout=3):
            return self.get_text(self.WARNING_ALERT)
        return ""

    def register_account(self, firstname, lastname, email, telephone, password):
        """Registers a new user account."""
        self.logger.info(f"Registering user account for: {email}")
        self.navigate_to(self.REGISTER_URL)
        self.send_keys(self.FIRSTNAME_INPUT, firstname)
        self.send_keys(self.LASTNAME_INPUT, lastname)
        self.send_keys(self.REG_EMAIL_INPUT, email)
        self.send_keys(self.TELEPHONE_INPUT, telephone)
        self.send_keys(self.REG_PASSWORD_INPUT, password)
        self.send_keys(self.CONFIRM_PASSWORD_INPUT, password)
        self.click(self.AGREE_CHECKBOX)
        self.click(self.CONTINUE_BUTTON)
        return self

    def ensure_logged_in(self, email, password, firstname="Capstone", lastname="Tester", telephone="9876543210"):
        """Attempts login; if account does not exist or login fails, creates a fresh test account."""
        self.open()
        if self.is_logged_in():
            self.logger.info("User already authenticated.")
            return self

        self.login(email, password)
        if self.is_logged_in():
            self.logger.info(f"User {email} authenticated successfully.")
            return self

        # Generate unique email to guarantee fresh registration success
        unique_email = f"capstone_{int(time.time())}@autotest.com"
        self.logger.warning(f"Default login failed. Auto-registering fresh test user: {unique_email}")
        self.register_account(firstname, lastname, unique_email, telephone, password)

        assert self.is_logged_in(), "User authentication failed even after auto-registration!"
        self.logger.info(f"Fresh user {unique_email} registered and authenticated successfully.")
        return self

