import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from config.config_reader import ConfigReader
from utilities.alert_handler import AlertHandler
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("TestCartOperations")

@pytest.mark.regression
class TestCartOperations:
    """Suite focusing on Cart operations, validation, and alert/popup handling."""

    def test_invalid_login_warning_alert(self, driver):
        """Verifies error alert appears on invalid login attempts."""
        import time
        logger.info("Running invalid login test...")
        login_page = LoginPage(driver)
        login_page.open()
        
        # Generate a unique invalid email on each run to prevent brute-force rate limiting
        unique_invalid_email = f"invalid_user_{int(time.time())}@fakeboxdemo.com"
        login_page.login(
            email=unique_invalid_email,
            password=ConfigReader.get_invalid_password()
        )
        login_page.capture_screenshot("invalid_login_attempt")
        warning = login_page.get_warning_message()
        
        # Accept standard mismatch or rate-limit security alert
        expected_warnings = [
            "Warning: No match for E-Mail Address and/or Password.",
            "Warning: Your account has exceeded allowed number of login attempts"
        ]
        assert any(w in warning for w in expected_warnings), f"Unexpected warning: '{warning}'"
        logger.info(f"Invalid login warning alert verified successfully: '{warning}'")

    def test_quantity_update_and_alert_handling(self, driver):
        """Verifies updating quantity and handling success alert popup."""
        logger.info("Running quantity update and alert dismissal test...")
        home_page = HomePage(driver)
        home_page.open()
        search_page = home_page.search_product("iPhone")
        search_page.add_product_to_cart("iPhone")

        cart_page = CartPage(driver)
        cart_page.open()

        # Update quantity to 4
        new_qty = 4
        alert_text = cart_page.update_quantity(new_qty=new_qty, product_name="iPhone")
        assert "Success: You have modified your shopping cart!" in alert_text

        # Verify alert dismissal
        alert_handler = AlertHandler(driver)
        dismissed = alert_handler.dismiss_bootstrap_alert()
        assert dismissed is True or not cart_page.is_displayed(cart_page.SUCCESS_ALERT, timeout=2)
        cart_page.capture_screenshot("alert_dismissed_check")

        # Verify recalculation
        unit_price = cart_page.get_unit_price("iPhone")
        line_total = cart_page.get_total_price("iPhone")
        expected_total = round(unit_price * new_qty, 2)
        assert abs(line_total - expected_total) < 0.05, f"Expected {expected_total}, got {line_total}"

    def test_cart_item_removal_and_empty_state(self, driver):
        """Verifies removing item from cart and empty cart message."""
        logger.info("Running cart removal test...")
        home_page = HomePage(driver)
        home_page.open()
        search_page = home_page.search_product("MacBook")
        search_page.add_product_to_cart("MacBook")

        cart_page = CartPage(driver)
        cart_page.open()
        assert cart_page.get_cart_items_count() > 0

        # Clear cart
        cart_page.clear_cart()
        cart_page.capture_screenshot("cart_cleared_state")
        assert cart_page.is_displayed(cart_page.EMPTY_CART_MESSAGE, timeout=5)
        logger.info("Cart cleared and empty message verified.")
