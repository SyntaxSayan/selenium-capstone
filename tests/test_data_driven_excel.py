import pytest
from pages.home_page import HomePage
from pages.cart_page import CartPage
from utilities.excel_util import ExcelUtil
from config.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("TestDataDrivenExcel")

def get_excel_test_data():
    excel_path = ConfigReader.get_excel_data_path()
    try:
        data = ExcelUtil.get_data_as_list_of_dicts(excel_path, "PurchaseScenarios")
        return data
    except Exception as e:
        logger.error(f"Failed to read test data from Excel: {e}")
        return []

@pytest.mark.datadriven
@pytest.mark.excel
class TestDataDrivenExcel:
    """
    Data-Driven Test Suite reading scenarios from Excel (openpyxl).
    Demonstrates parameterization, external test data management,
    search, add-to-cart, quantity updates, and cart assertions.
    """

    @pytest.mark.parametrize("scenario", get_excel_test_data())
    def test_ecommerce_excel_driven_scenario(self, driver, scenario):
        test_id = scenario.get("TestID")
        desc = scenario.get("Description")
        search_term = scenario.get("SearchTerm")
        product_name = scenario.get("ProductName")
        updated_qty = int(scenario.get("UpdatedQty", 2))

        logger.info(f"----- Running Excel Driven Test [{test_id}]: {desc} -----")

        # Step 1: Open Home Page
        home_page = HomePage(driver)
        home_page.open()

        # Step 2: Search for product
        search_page = home_page.search_product(search_term)
        assert search_page.get_products_count() > 0, f"[{test_id}] No products found for '{search_term}'"

        # Step 3: Add product to cart
        alert = search_page.add_product_to_cart(product_name=product_name)
        assert "Success: You have added" in alert, f"[{test_id}] Failed to add product to cart!"
        search_page.capture_screenshot(f"excel_{test_id}_product_added")

        # Step 4: Open Cart
        cart_page = CartPage(driver)
        cart_page.open()
        assert cart_page.is_product_in_cart(product_name), f"[{test_id}] Product '{product_name}' not in cart!"

        # Step 5: Update Quantity
        update_msg = cart_page.update_quantity(new_qty=updated_qty, product_name=product_name)
        assert "Success: You have modified your shopping cart!" in update_msg
        cart_page.capture_screenshot(f"excel_{test_id}_qty_updated")

        # Step 6: Verify Cart Details
        actual_qty = cart_page.get_quantity(product_name)
        assert actual_qty == updated_qty, f"[{test_id}] Quantity mismatch! Expected: {updated_qty}, Actual: {actual_qty}"

        unit_price = cart_page.get_unit_price(product_name)
        total_price = cart_page.get_total_price(product_name)
        assert unit_price > 0, f"[{test_id}] Invalid unit price: {unit_price}"
        expected_total = round(unit_price * updated_qty, 2)
        assert abs(total_price - expected_total) < 0.05, f"[{test_id}] Total mismatch! Expected: {expected_total}, Got: {total_price}"

        # Step 7: Dismiss Alert
        cart_page.dismiss_alert()
        logger.info(f"[{test_id}] Completed successfully with verified total: ${total_price}")
