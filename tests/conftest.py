import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger
from utilities.screenshot_util import ScreenshotUtil

logger = CustomLogger.get_logger("Conftest")

def pytest_addoption(parser):
    """Add custom CLI options for browser and headless mode."""
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser type: chrome | edge | firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )

@pytest.fixture(scope="function")
def driver(request):
    """Initializes and provides the Selenium WebDriver instance with teardown."""
    cli_browser = request.config.getoption("--browser")
    cli_headless = request.config.getoption("--headless")

    browser = (cli_browser or ConfigReader.get_browser()).strip().lower()
    is_headless = cli_headless or ConfigReader.get_headless()

    logger.info(f"Setting up WebDriver: Browser='{browser}', Headless={is_headless}")

    driver_instance = None

    if browser == "chrome":
        options = ChromeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        driver_instance = webdriver.Chrome(options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        driver_instance = webdriver.Edge(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if is_headless:
            options.add_argument("-headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver_instance = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported browser specified: '{browser}'. Supported: chrome, edge, firefox")

    driver_instance.implicitly_wait(ConfigReader.get_implicit_wait())
    driver_instance.set_page_load_timeout(ConfigReader.get_page_load_timeout())
    if not is_headless:
        try:
            driver_instance.maximize_window()
        except Exception:
            pass

    # Attach driver to test class/instance if used
    if request.cls is not None:
        request.cls.driver = driver_instance

    # Keep a reference on request.node for failure screenshot hook
    request.node.driver = driver_instance

    yield driver_instance

    logger.info("Tearing down WebDriver instance.")
    try:
        driver_instance.quit()
    except Exception as e:
        logger.warning(f"Error while quitting driver: {e}")

# ----------------- PYTEST HTML REPORT CUSTOMIZATION & SCREENSHOTS ----------------- #

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures screenshot on failure and attaches it to the HTML report."""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver = getattr(item, "driver", None)
        if driver:
            try:
                test_name = item.name.replace("[", "_").replace("]", "_")
                screenshot_path = ScreenshotUtil.capture_screenshot(driver, f"FAIL_{test_name}")
                if screenshot_path and os.path.exists(screenshot_path):
                    import pytest_html
                    # Add relative screenshot path to report extras
                    rel_path = os.path.relpath(screenshot_path, ConfigReader.get_report_dir())
                    extras.append(pytest_html.extras.image(rel_path))
                    logger.info(f"Attached failure screenshot to report: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to capture failure screenshot: {e}")

    report.extras = extras

def pytest_html_report_title(report):
    """Custom title for the HTML execution report."""
    report.title = "Capstone Project: E-Commerce Selenium Automation Report"

def pytest_metadata(metadata):
    """Enrich HTML report environment metadata."""
    metadata["Project Name"] = "Capstone Assignment 1 - Selenium WebDriver with Python"
    metadata["Application Under Test"] = "TutorialsNinja E-Commerce Demo"
    metadata["Framework Architecture"] = "Page Object Model (POM) + Pytest + Data-Driven"
    metadata["Test Types"] = "E2E, Data-Driven (Excel/JSON), Cart Ops, Alerts & Popups"
    metadata["Tester / Author"] = "Quality Engineering Automation Team"
    metadata["Execution Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
