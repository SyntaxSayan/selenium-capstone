from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductDetailPage(BasePage):
    """Page Object for TutorialsNinja Product Details Page."""

    PRODUCT_TITLE = (By.XPATH, "//div[@id='content']//h1")
    PRICE_HEADER = (By.XPATH, "//div[@id='content']//ul[contains(@class, 'list-unstyled')][2]//h2")
    QUANTITY_INPUT = (By.ID, "input-quantity")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    SHOPPING_CART_LINK_IN_ALERT = (By.XPATH, "//div[contains(@class, 'alert-success')]//a[text()='shopping cart']")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_title(self):
        """Returns the product heading title."""
        return self.get_text(self.PRODUCT_TITLE)

    def set_quantity(self, quantity):
        """Sets the quantity on product detail page."""
        self.send_keys(self.QUANTITY_INPUT, str(quantity))

    def add_to_cart(self):
        """Clicks 'Add to Cart' button and waits for success notification."""
        self.click(self.ADD_TO_CART_BUTTON)
        alert = self.wait_for_visible(self.SUCCESS_ALERT, timeout=10)
        return alert.text.strip()

    def go_to_cart_from_alert(self):
        """Clicks shopping cart link in success alert."""
        self.click(self.SHOPPING_CART_LINK_IN_ALERT)
        from pages.cart_page import CartPage
        return CartPage(self.driver)
