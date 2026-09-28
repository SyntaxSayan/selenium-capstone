from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config_reader import ConfigReader

class HomePage(BasePage):
    """Page Object for TutorialsNinja Home Page."""

    # Locators
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    MY_ACCOUNT_DROPDOWN = (By.XPATH, "//a[@title='My Account']")
    LOGIN_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu')]//a[text()='Login']")
    REGISTER_OPTION = (By.XPATH, "//ul[contains(@class, 'dropdown-menu')]//a[text()='Register']")
    SHOPPING_CART_LINK = (By.XPATH, "//a[@title='Shopping Cart']")
    CART_BUTTON = (By.ID, "cart-total")
    CART_VIEW_CART_LINK = (By.XPATH, "//strong[contains(text(), 'View Cart')]")
    LOGO = (By.CSS_SELECTOR, "#logo a")

    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = ConfigReader.get_base_url()

    def open(self):
        """Opens the home page URL."""
        self.navigate_to(self.base_url)
        return self

    def search_product(self, search_term):
        """Types product search term and clicks search button."""
        self.logger.info(f"Searching for product: '{search_term}'")
        self.send_keys(self.SEARCH_INPUT, search_term)
        self.click(self.SEARCH_BUTTON)
        from pages.search_results_page import SearchResultsPage
        return SearchResultsPage(self.driver)

    def navigate_to_login(self):
        """Navigates to Login page via My Account dropdown."""
        self.click(self.MY_ACCOUNT_DROPDOWN)
        self.click(self.LOGIN_OPTION)
        from pages.login_page import LoginPage
        return LoginPage(self.driver)

    def navigate_to_register(self):
        """Navigates to Register page via My Account dropdown."""
        self.click(self.MY_ACCOUNT_DROPDOWN)
        self.click(self.REGISTER_OPTION)
        return self

    def navigate_to_shopping_cart(self):
        """Clicks top header Shopping Cart link."""
        self.click(self.SHOPPING_CART_LINK)
        from pages.cart_page import CartPage
        return CartPage(self.driver)
