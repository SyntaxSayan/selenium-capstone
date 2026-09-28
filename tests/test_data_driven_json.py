import pytest
from pages.home_page import HomePage
from pages.cart_page import CartPage
from utilities.json_util import JsonUtil
from config.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("TestDataDrivenJson")

def get_json_test_data():
    json_path = ConfigReader.get_json_data_path()
    try:
        return JsonUtil.get_test_cases(json_path)
    except Exception as e:
        logger.error(f"Failed to read test data from JSON: {e}")
        return []

@pytest.mark.datadriven
@pytest.mark.json
class TestDataDrivenJson:
    """
    Data-Driven Test Suite reading scenarios from JSON.
    Validates product search, cart addition, quantity updates,
    and cart calculations for various products.
    """

    @pytest.mark.parametrize("case", get_json_test_data())
    def test_ecommerce_json_driven_scenario(self, driver, case):
        test_id = case.get("test_id")
        desc = case.get("description")
        search_term = case.get("search_term")
        product_name = case.get("product_name")
        updated_qty = int(case.get("updated_qty", 2))

        logger.info(f"----- Running JSON Driven Test [{test_id}]: {desc} -----")

        # Step 1: Open Home Page
        home_page = HomePage(driver)
        home_page.open()

        # Step 2: Search for product
        search_page = home_page.search_product(search_term)
        assert search_page.get_products_count() > 0, f"[{test_id}] Product '{search_term}' not found in search."

        # Step 3: Add to cart
        alert = search_page.add_product_to_cart(product_name=product_name)
        assert "Success: You have added" in alert
        search_page.capture_screenshot(f"json_{test_id}_product_added")

        # Step 4: Open Cart
        cart_page = CartPage(driver)
        cart_page.open()
        assert cart_page.is_product_in_cart(product_name)

        # Step 5: Update quantity
        cart_page.update_quantity(new_qty=updated_qty, product_name=product_name)
        cart_page.capture_screenshot(f"json_{test_id}_qty_updated")

        # Step 6: Verify cart
        actual_qty = cart_page.get_quantity(product_name)
        assert actual_qty == updated_qty, f"[{test_id}] Expected qty {updated_qty}, got {actual_qty}"

        unit_price = cart_page.get_unit_price(product_name)
        line_total = cart_page.get_total_price(product_name)
        assert unit_price > 0
        expected_total = round(unit_price * updated_qty, 2)
        assert abs(line_total - expected_total) < 0.05, f"[{test_id}] Total mismatch! Expected {expected_total}, got {line_total}"

        # Step 7: Dismiss alert
        cart_page.dismiss_alert()
        logger.info(f"[{test_id}] JSON-driven test passed successfully.")
