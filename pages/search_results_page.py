from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SearchResultsPage(BasePage):
    """Page Object for TutorialsNinja Search Results Page."""

    # Locators
    SEARCH_HEADING = (By.XPATH, "//div[@id='content']//h1[contains(text(), 'Search')]")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-layout")
    PRODUCT_TITLE = (By.XPATH, ".//div[@class='caption']//h4/a")
    ADD_TO_CART_BUTTON = (By.XPATH, ".//button[contains(@onclick, 'cart.add')]")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    SUCCESS_ALERT_CART_LINK = (By.XPATH, "//div[contains(@class, 'alert-success')]//a[text()='shopping cart']")
    ALERT_CLOSE_BUTTON = (By.CSS_SELECTOR, ".alert-success button.close")
    NO_RESULTS_MESSAGE = (By.XPATH, "//p[contains(text(), 'There is no product that matches the search criteria.')]")

    def __init__(self, driver):
        super().__init__(driver)

    def get_products_count(self):
        """Returns the number of products listed in search results."""
        products = self.find_all(self.PRODUCT_CARDS)
        return len(products)

    def get_all_product_titles(self):
        """Returns list of product titles displayed on search page."""
        cards = self.find_all(self.PRODUCT_CARDS)
        titles = []
        for card in cards:
            title_elem = card.find_element(*self.PRODUCT_TITLE)
            titles.append(title_elem.text.strip())
        return titles

    def is_product_listed(self, product_name):
        """Verifies if a product with the specified name is in results."""
        titles = self.get_all_product_titles()
        matched = any(product_name.lower() in t.lower() for t in titles)
        self.logger.info(f"Checking if '{product_name}' is in results: {matched}")
        return matched

    def add_product_to_cart(self, product_name=None):
        """
        Clicks 'Add to Cart' for a matching product name, or the first product if None.
        Waits for success notification banner to appear.
        """
        cards = self.find_all(self.PRODUCT_CARDS)
        if not cards:
            raise Exception("No product cards found in search results to add to cart.")

        target_card = cards[0]
        if product_name:
            found = False
            for card in cards:
                title = card.find_element(*self.PRODUCT_TITLE).text.strip()
                if product_name.lower() in title.lower():
                    target_card = card
                    found = True
                    break
            if not found:
                self.logger.warning(f"Product '{product_name}' not exact match; falling back to first item.")

        add_btn = target_card.find_element(*self.ADD_TO_CART_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
        self.driver.execute_script("arguments[0].click();", add_btn)
        self.logger.info("Clicked 'Add to Cart' button.")

        # Wait for success banner
        alert = self.wait_for_visible(self.SUCCESS_ALERT, timeout=10)
        text = alert.text.strip()
        self.logger.info(f"Add to cart alert: '{text}'")
        return text

    def get_success_message(self):
        """Gets text from the success notification banner."""
        if self.is_displayed(self.SUCCESS_ALERT, timeout=5):
            return self.get_text(self.SUCCESS_ALERT)
        return ""

    def dismiss_success_alert(self):
        """Clicks close button on the success banner."""
        if self.is_displayed(self.ALERT_CLOSE_BUTTON, timeout=3):
            self.click(self.ALERT_CLOSE_BUTTON)
            self.logger.info("Dismissed success alert.")

    def open_cart_from_alert(self):
        """Clicks the 'shopping cart' link within the success notification banner."""
        self.click(self.SUCCESS_ALERT_CART_LINK)
        from pages.cart_page import CartPage
        return CartPage(self.driver)
