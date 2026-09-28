import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from config.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("TestE2EPurchase")

@pytest.mark.e2e
class TestE2EPurchase:
    """
    End-to-End E-Commerce Purchase Flow.
    Covers:
      1. Launch browser
      2. Login to application
      3. Search product
      4. Add product to cart
      5. Update quantity
      6. Verify cart details
      7. Capture step-by-step screenshots
      8. Handle popup / alert notifications
    """

    def test_complete_ecommerce_purchase_flow(self, driver):
        logger.info("========== Starting E2E Purchase Flow Test ==========")

        # Step 1: Open Application
        home_page = HomePage(driver)
        home_page.open()
        home_page.capture_screenshot("01_home_page_launched")
        assert "Your Store" in home_page.get_title(), "Home page title mismatch!"

        # Step 2: Login to Application
        login_page = LoginPage(driver)
        valid_email = ConfigReader.get_valid_email()
        valid_password = ConfigReader.get_valid_password()
        first_name = ConfigReader.get_user_firstname()
        last_name = ConfigReader.get_user_lastname()
        telephone = ConfigReader.get_user_telephone()

        login_page.ensure_logged_in(
            email=valid_email,
            password=valid_password,
            firstname=first_name,
            lastname=last_name,
            telephone=telephone
        )
        login_page.capture_screenshot("02_user_logged_in")
        assert login_page.is_logged_in(), "User failed to authenticate!"
        logger.info("Step 2 passed: User authenticated successfully.")

        # Step 3: Search Product
        search_term = "MacBook"
        search_results_page = home_page.search_product(search_term)
        search_results_page.capture_screenshot("03_search_results")
        assert search_results_page.get_products_count() > 0, f"No products found for search: '{search_term}'"
        assert search_results_page.is_product_listed(search_term), f"Expected product '{search_term}' not listed in results!"
        logger.info(f"Step 3 passed: Product '{search_term}' found in search results.")

        # Step 4: Add Product to Cart & Verify Alert Banner
        alert_msg = search_results_page.add_product_to_cart(product_name=search_term)
        search_results_page.capture_screenshot("04_product_added_to_cart")
        assert "Success: You have added" in alert_msg, f"Unexpected alert message: '{alert_msg}'"
        logger.info(f"Step 4 passed: Product added with alert: '{alert_msg}'")

        # Step 5: Navigate to Cart
        cart_page = CartPage(driver)
        cart_page.open()
        cart_page.capture_screenshot("05_cart_initial_view")
        assert cart_page.is_product_in_cart(search_term), f"Product '{search_term}' not found in cart!"
        initial_qty = cart_page.get_quantity(search_term)
        logger.info(f"Initial quantity in cart: {initial_qty}")
        assert initial_qty >= 1, "Initial quantity should be at least 1."

        # Step 6: Update Quantity
        new_quantity = 2
        update_alert = cart_page.update_quantity(new_qty=new_quantity, product_name=search_term)
        cart_page.capture_screenshot("06_quantity_updated")
        assert "Success: You have modified your shopping cart!" in update_alert, f"Unexpected cart update alert: '{update_alert}'"
        logger.info("Step 6 passed: Quantity updated with success alert.")

        # Step 7: Verify Cart Details
        updated_qty = cart_page.get_quantity(search_term)
        unit_price = cart_page.get_unit_price(search_term)
        line_total = cart_page.get_total_price(search_term)

        logger.info(f"Verification -> Quantity: {updated_qty}, Unit Price: ${unit_price}, Line Total: ${line_total}")
        assert updated_qty == new_quantity, f"Expected quantity {new_quantity}, but got {updated_qty}"
        assert unit_price > 0, "Unit price should be greater than 0."
        expected_line_total = round(unit_price * new_quantity, 2)
        assert abs(line_total - expected_line_total) < 0.05, f"Line total mismatch! Expected ${expected_line_total}, got ${line_total}"

        # Step 8: Handle Popup / Dismiss Alert Banner
        cart_page.dismiss_alert()
        cart_page.capture_screenshot("07_cart_verified_alert_dismissed")
        logger.info("Step 8 passed: Alert banner dismissed successfully.")

        # Step 9: Final Totals Verification
        final_total = cart_page.get_final_total()
        logger.info(f"Final Cart Total: ${final_total}")
        assert final_total >= line_total, f"Final total (${final_total}) should be >= line total (${line_total})"

        logger.info("========== E2E Purchase Flow Test COMPLETED SUCCESSFULLY ==========")
