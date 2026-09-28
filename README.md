Video Demonstration Link: https://www.loom.com/share/8d5cbc9d342648b9b790a8c2944b7147

# Selenium Python Framework - PyTest + POM

Automates Login, Product Search, Cart Operations, and End-to-End Checkout on the TutorialsNinja demo store (https://tutorialsninja.com/demo/).

## Project structure

```
AUTOMATION/
├── config/
│   ├── config.ini              # URL, browser, waits, credentials, folder paths
│   └── config_reader.py        # reads config.ini with environment overrides
├── pages/                      # Page Object Model
│   ├── base_page.py            #   waits, click, type, logging (parent class)
│   ├── home_page.py            #   header search + navigation to login & cart
│   ├── login_page.py           #   authentication & auto-registration fallback
│   ├── search_results_page.py  #   search results & add to cart
│   ├── product_detail_page.py  #   product details & quantity selection
│   └── cart_page.py            #   quantity updater, item removal, price checks
├── utilities/                  # Utility classes
│   ├── custom_logger.py        #   console + logs/automation.log
│   ├── screenshot_util.py      #   timestamped & failure screenshot helper
│   ├── alert_handler.py        #   JavaScript dialog & DOM alert/modal popup utility
│   ├── excel_util.py           #   openpyxl reader for Excel test data
│   └── json_util.py            #   JSON reader for test datasets
├── test_data/                  # External test data files
│   ├── test_data.xlsx          #   Excel dataset (parameterized purchase scenarios)
│   ├── test_data.json          #   JSON dataset
│   └── create_excel_data.py    #   script to generate/rebuild Excel data
├── tests/
│   ├── conftest.py             #   fixtures, CLI flags (--browser, --headless) + failure hook
│   ├── test_e2e_purchase.py    #   complete End-to-End purchase flow
│   ├── test_data_driven_excel.py # data-driven tests via Excel (openpyxl)
│   ├── test_data_driven_json.py  # data-driven tests via JSON
│   └── test_cart_operations.py #   cart operations, quantity updates, alert handling
├── reports/                    # HTML reports (report.html)
├── screenshots/                # Step-by-step & failure PNG captures
├── logs/                       # Execution logs (automation.log)
├── pytest.ini                  # Pytest configuration & CLI options
├── requirements.txt            # Project dependencies
├── run_tests.bat               # One-click Windows batch runner
└── run_tests.ps1               # Configurable PowerShell execution runner
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # Python 3.10+, Chrome/Firefox/Edge installed
```

Selenium 4.6+ downloads the browser driver automatically (no webdriver-manager needed).

Test credentials and environment configurations are centralized in `config/config.ini`. Update credentials or base URL if testing custom accounts:

```ini
[common_info]
base_url = https://tutorialsninja.com/demo/
browser = chrome
headless = false
```

## Running the tests

```bash
# PyTest (HTML report: reports/report.html)
pytest
pytest --headless
pytest --browser firefox --headless
pytest tests/test_e2e_purchase.py
pytest tests/test_data_driven_excel.py
pytest tests/test_data_driven_json.py
pytest tests/test_cart_operations.py -k test_invalid_login

# Windows One-Click Batch Runner
run_tests.bat

# PowerShell Runner with Parameters
.\run_tests.ps1 -Headless
.\run_tests.ps1 -Browser edge -Headless
```

## How each requirement is covered

| Requirement | Where |
|---|---|
| Launch Browser & Cross-Browser | `utilities/` & `tests/conftest.py` - Chrome, Firefox, Edge; headed & headless modes via CLI flags (`--browser`, `--headless`) and `config.ini` |
| Login to Application | `pages/login_page.py` - user authentication, session validation, and auto-registration fallback |
| Search Product | `pages/home_page.py`, `pages/search_results_page.py` - search bar locators, auto-suggest, and product card validation |
| Add Product to Cart | `pages/search_results_page.py`, `pages/product_detail_page.py` - explicit waits, JavaScript fallback click, and success banner verification |
| Update Quantity | `pages/cart_page.py` - quantity field input update, button submit, and cart recalculation |
| Verify Cart Details | `pages/cart_page.py` - mathematical assertions on unit price, quantity, line total ($Price \times Qty$), and order total |
| Screenshot on Failure & Steps | `utilities/screenshot_util.py`, `tests/conftest.py` - timestamped step captures in `screenshots/`, and `pytest_runtest_makereport` hook attaches failure screenshots to the HTML report |
| Test Data (Excel & JSON) | `utilities/excel_util.py` (reads `test_data/test_data.xlsx`), `utilities/json_util.py` (reads `test_data/test_data.json`) - parameterized with `@pytest.mark.parametrize` |
| Handle Popup / Alerts | `utilities/alert_handler.py` - native JavaScript dialogs (`alert`, `confirm`, `prompt`) and dismissible DOM / Bootstrap modal banners |
| HTML Reporting | `pytest-html` via `pytest.ini` & `tests/conftest.py` -> `reports/report.html` (self-contained, metadata enriched, screenshots embedded) |
| Logging | `utilities/custom_logger.py` -> console + `logs/automation.log` (passwords are never logged) |

## Design notes (useful for the viva)

- **Explicit waits only** - no `time.sleep`, no implicit wait (mixing the two causes unpredictable timeouts). Elements are synchronized dynamically with `WebDriverWait` and `expected_conditions`.
- **Fresh browser per test** - tests are independent and can run in any order with function-scoped fixtures in `conftest.py`.
- **POM navigation methods return the next page object**, e.g. `HomePage.search_for()` returns `SearchResultsPage`.
- **Resilient click fallback** - if an element is overlapped or animated (`ElementClickInterceptedException`), the framework automatically falls back to JavaScript execution (`execute_script`).
- **Data-driven testing** - parameterized using `@pytest.mark.parametrize` reading from Excel (`openpyxl`) and JSON; each row gets its own result line, browser session, and screenshot.
- **Failure detection & reporting** - `pytest_runtest_makereport` hook in `conftest.py` captures the browser screenshot dynamically on failure before teardown and embeds it into the self-contained HTML report.

## Notes and limitations

- The demo is a public shared site (`https://tutorialsninja.com/demo/`); if it is slow or resets its database, test user credentials in `config/config.ini` can be updated or the auto-registration fallback in `login_page.py` will self-heal.
- OpenCart temporarily locks an account after several failed logins with the same e-mail. The negative login tests therefore verify error alert banners or rate-limiting warnings cleanly.
- Locators were written from the standard OpenCart 3 markup that TutorialsNinja uses. If the site changes its markup, only the locator constants in `pages/` need updating.
