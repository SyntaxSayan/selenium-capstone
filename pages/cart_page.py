import re
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """Page Object for TutorialsNinja Shopping Cart Page."""

    CART_URL = "https://tutorialsninja.com/demo/index.php?route=checkout/cart"

    # Locators
    CART_HEADING = (By.XPATH, "//div[@id='content']//h1[contains(text(), 'Shopping Cart')]")
    CART_ROWS = (By.XPATH, "//div[@id='content']//form//table//tbody//tr")
    PRODUCT_NAME_CELL = (By.XPATH, ".//td[2]")
    PRODUCT_NAME_LINK = (By.XPATH, ".//td[2]/a")
    QUANTITY_INPUT = (By.XPATH, ".//td[4]//input[starts-with(@name, 'quantity')]")
    UPDATE_BUTTON = (By.XPATH, ".//td[4]//button[@data-original-title='Update' or @type='submit']")
    REMOVE_BUTTON = (By.XPATH, ".//td[4]//button[contains(@data-original-title, 'Remove') or contains(@onclick, 'cart.remove')]")
    UNIT_PRICE_CELL = (By.XPATH, ".//td[5]")
    TOTAL_PRICE_CELL = (By.XPATH, ".//td[6]")
    
    # Alert / Notification
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert-success")
    ALERT_CLOSE_BUTTON = (By.CSS_SELECTOR, ".alert-success button.close")
    WARNING_ALERT = (By.CSS_SELECTOR, ".alert-danger")

    # Totals Section
    TOTAL_SUMMARY_ROWS = (By.XPATH, "//div[@id='content']//div[contains(@class, 'col-sm-4')]//table//tr")
    CHECKOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Checkout') and contains(@class, 'btn-primary')]")
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[@id='content']//p[contains(text(), 'Your shopping cart is empty!')]")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Navigates directly to the Shopping Cart page."""
        self.navigate_to(self.CART_URL)
        return self

    def _find_target_row(self, product_name=None):
        """Finds row corresponding to product name, or returns first row."""
        rows = self.find_all(self.CART_ROWS)
        if not rows:
            raise Exception("Shopping cart is empty; no product rows found.")

        if not product_name:
            return rows[0]

        for row in rows:
            text = row.find_element(*self.PRODUCT_NAME_CELL).text
            if product_name.lower() in text.lower():
                return row
        return rows[0]

    def get_cart_items_count(self):
        """Returns number of unique line items in cart."""
        return len(self.find_all(self.CART_ROWS))

    def is_product_in_cart(self, product_name):
        """Checks if a product is in cart."""
        rows = self.find_all(self.CART_ROWS)
        for row in rows:
            text = row.find_element(*self.PRODUCT_NAME_CELL).text
            if product_name.lower() in text.lower():
                return True
        return False

    def get_quantity(self, product_name=None):
        """Gets current quantity value from input box."""
        row = self._find_target_row(product_name)
        qty_input = row.find_element(*self.QUANTITY_INPUT)
        val = qty_input.get_attribute("value")
        return int(val) if val and val.isdigit() else 0

    def update_quantity(self, new_qty, product_name=None):
        """Updates quantity input and clicks Update button, then waits for success alert."""
        self.logger.info(f"Updating quantity to: {new_qty} for product: '{product_name}'")
        row = self._find_target_row(product_name)
        qty_input = row.find_element(*self.QUANTITY_INPUT)
        qty_input.clear()
        qty_input.send_keys(str(new_qty))

        update_btn = row.find_element(*self.UPDATE_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", update_btn)
        self.driver.execute_script("arguments[0].click();", update_btn)

        # Wait for update success banner
        alert = self.wait_for_visible(self.SUCCESS_ALERT, timeout=10)
        msg = alert.text.strip()
        self.logger.info(f"Quantity updated successfully. Alert: '{msg}'")
        return msg

    def get_unit_price(self, product_name=None):
        """Gets unit price as float."""
        row = self._find_target_row(product_name)
        price_text = row.find_element(*self.UNIT_PRICE_CELL).text.strip()
        cleaned = re.sub(r"[^\d.]", "", price_text)
        return float(cleaned) if cleaned else 0.0

    def get_total_price(self, product_name=None):
        """Gets line item total price as float."""
        row = self._find_target_row(product_name)
        total_text = row.find_element(*self.TOTAL_PRICE_CELL).text.strip()
        cleaned = re.sub(r"[^\d.]", "", total_text)
        return float(cleaned) if cleaned else 0.0

    def get_final_total(self):
        """Reads final order Total from summary table."""
        rows = self.find_all(self.TOTAL_SUMMARY_ROWS)
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2:
                header = cells[0].text.strip()
                if header == "Total:" or (header.endswith("Total:") and "Sub-Total" not in header):
                    cleaned = re.sub(r"[^\d.]", "", cells[1].text.strip())
                    return float(cleaned) if cleaned else 0.0
        return 0.0

    def get_subtotal(self):
        """Reads Sub-Total from summary table."""
        rows = self.find_all(self.TOTAL_SUMMARY_ROWS)
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 2 and "Sub-Total" in cells[0].text:
                cleaned = re.sub(r"[^\d.]", "", cells[1].text.strip())
                return float(cleaned) if cleaned else 0.0
        return 0.0

    def get_alert_message(self):
        """Returns message of success/warning alert."""
        if self.is_displayed(self.SUCCESS_ALERT, timeout=3):
            return self.get_text(self.SUCCESS_ALERT)
        if self.is_displayed(self.WARNING_ALERT, timeout=3):
            return self.get_text(self.WARNING_ALERT)
        return ""

    def dismiss_alert(self):
        """Dismisses the success notification banner."""
        if self.is_displayed(self.ALERT_CLOSE_BUTTON, timeout=3):
            self.click(self.ALERT_CLOSE_BUTTON)
            self.logger.info("Dismissed alert banner.")

    def clear_cart(self):
        """Removes all items from cart."""
        while True:
            rows = self.find_all(self.CART_ROWS, timeout=2)
            if not rows:
                break
            try:
                remove_btn = rows[0].find_element(*self.REMOVE_BUTTON)
                remove_btn.click()
            except Exception:
                break
        self.logger.info("Cart cleared.")
