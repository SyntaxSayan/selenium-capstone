# Capstone Assignment 1: E-Commerce Automation Framework
### Automated Web Testing Using Selenium WebDriver with Python & Pytest

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green?logo=selenium)
![Pytest](https://img.shields.io/badge/Pytest-9.x-orange?logo=pytest)
![Report](https://img.shields.io/badge/HTML%20Report-Self--Contained-brightgreen)
![Design](https://img.shields.io/badge/Pattern-Page%20Object%20Model-purple)

---

## 1. Project Overview & Business Scenario

This enterprise-grade automation framework automates the end-to-end shopping workflow on the **TutorialsNinja E-Commerce Demo Application** (`https://tutorialsninja.com/demo/`). It is engineered to meet and exceed all requirements of **Capstone Assignment 1**, following industry standards including the **Page Object Model (POM)** pattern, **Data-Driven Testing (Excel & JSON)**, robust **Alert & Popup Handling**, **Step-by-step & Failure Screenshot Captures**, and rich **HTML Execution Reporting**.

### Business Scenario
> *A customer wants to purchase a product from an E-Commerce site.*

### Requirements Traceability Matrix

| # | Capstone Requirement | Framework Implementation | Verified Status |
|---|----------------------|--------------------------|-----------------|
| 1 | **Launch Browser** | Cross-browser driver factory supporting Chrome, Edge, and Firefox with Headless & Headed modes via `conftest.py` & `config.ini`. | ✅ PASSED |
| 2 | **Login to Application** | `LoginPage` implementing robust login, session validation, and auto-registration fallback to ensure 100% test reliability. | ✅ PASSED |
| 3 | **Search Product** | `HomePage` and `SearchResultsPage` with dynamic search bar locator, presence validation, and product card matching. | ✅ PASSED |
| 4 | **Add Product to Cart** | Add-to-cart action with explicit waits (`WebDriverWait` + `EC`), JS click fallback, and notification alert verification. | ✅ PASSED |
| 5 | **Update Quantity** | `CartPage` quantity input modification with update button submission and refresh verification. | ✅ PASSED |
| 6 | **Verify Cart Details** | Mathematical assertions on unit price, updated quantity, calculated line total ($Price \times Qty$), subtotal, and final order total. | ✅ PASSED |
| 7 | **Capture Screenshots** | `ScreenshotUtil` captures timestamped PNGs for every critical step into `screenshots/`, plus automatic failure screenshots attached directly to the HTML report. | ✅ PASSED |
| 8 | **Read Test Data from Excel / JSON** | `ExcelUtil` (`openpyxl`) reads `test_data/test_data.xlsx`; `JsonUtil` reads `test_data/test_data.json` for parameterized test suites. | ✅ PASSED |
| 9 | **Handle Popup / Alerts if Available** | `AlertHandler` handles native browser JavaScript dialogs (`alert`, `confirm`, `prompt`) and dismissible DOM modal / Bootstrap banner notifications. | ✅ PASSED |
| 10| **Generate Execution Report** | `pytest-html` generates comprehensive, self-contained interactive report at `reports/report.html` with environment metadata, metrics, and screenshots. | ✅ PASSED |

---

## 2. Framework Architecture & Design Pattern

The framework utilizes a decoupled, layered **Page Object Model (POM)** architecture:

```
                                    +-----------------------+
                                    |    pytest.ini / CLI   |
                                    +-----------+-----------+
                                                |
                                    +-----------v-----------+
                                    |   tests/conftest.py   |
                                    |  (Driver, Fixtures,   |
                                    |  Report Customization)|
                                    +-----------+-----------+
                                                |
                      +-------------------------+-------------------------+
                      |                                                   |
           +----------v----------+                             +----------v----------+
           |     Test Suites     |                             |     Page Objects    |
           |---------------------|                             |---------------------|
           | test_e2e_purchase   |                             | BasePage            |
           | test_data_driven_xl | <--------- actions -------> | HomePage            |
           | test_data_driven_js |                             | LoginPage           |
           | test_cart_ops       |                             | SearchResultsPage   |
           +----------+----------+                             | CartPage            |
                      |                                        | ProductDetailPage   |
                      |                                        +----------+----------+
                      |                                                   |
           +----------v----------+                             +----------v----------+
           |      Utilities      |                             |      Test Data      |
           |---------------------|                             |---------------------|
           | CustomLogger        |                             | test_data.xlsx      |
           | ScreenshotUtil      |                             | test_data.json      |
           | AlertHandler        |                             | config.ini          |
           | ExcelUtil (openpyxl)|                             +---------------------+
           | JsonUtil            |
           +---------------------+
```

### Key Architectural Strengths:
1. **Explicit Waits (`WebDriverWait`)**: Eliminates flaky tests caused by network latency or DOM re-rendering.
2. **Resilient Click Fallback**: If an element is overlapped or animated (`ElementClickInterceptedException`), the framework automatically falls back to JavaScript execution (`execute_script`).
3. **Self-Contained Reporting**: The HTML execution report embeds CSS and resources into a single file suitable for emailing or CI/CD pipelines.

---

## 3. Directory Structure

```
AUTOMATION/
│
├── config/
│   ├── __init__.py
│   ├── config.ini                     # Base URLs, timeouts, browser defaults, test credentials
│   └── config_reader.py               # Robust configuration parser
│
├── test_data/
│   ├── test_data.json                 # JSON parameterized test scenarios
│   ├── test_data.xlsx                 # Excel test dataset with formatted columns
│   └── create_excel_data.py           # Script to generate/rebuild the Excel dataset
│
├── utilities/
│   ├── __init__.py
│   ├── custom_logger.py               # File and console logger (writes to logs/automation.log)
│   ├── screenshot_util.py             # Timestamped screenshot generator
│   ├── alert_handler.py               # JavaScript dialog & DOM alert/modal popup utility
│   ├── excel_util.py                  # openpyxl reader returning lists of dictionaries
│   └── json_util.py                   # JSON reader utility
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py                   # Core POM foundation with waits, actions, and JS fallbacks
│   ├── home_page.py                   # Search bar, header navigation, cart shortcuts
│   ├── login_page.py                  # Authentication, warnings, registration self-healing
│   ├── search_results_page.py         # Product cards, titles, add-to-cart triggers
│   ├── product_detail_page.py         # Detailed product view & quantity selection
│   └── cart_page.py                   # Quantity updater, item removal, price assertions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Cross-browser fixtures, failure hooks, report enrichment
│   ├── test_e2e_purchase.py           # Complete End-to-End purchase flow
│   ├── test_data_driven_excel.py      # Data-driven suite reading from Excel
│   ├── test_data_driven_json.py       # Data-driven suite reading from JSON
│   └── test_cart_operations.py        # Granular cart ops, quantity changes, alert handling
│
├── reports/
│   └── report.html                    # Generated interactive execution report
├── screenshots/                       # Step-by-step & failure PNG captures
├── logs/
│   └── automation.log                 # Detailed timestamped execution log
│
├── pytest.ini                         # Pytest configuration & report flags
├── requirements.txt                   # Dependency list
├── run_tests.bat                      # One-click Windows batch runner
├── run_tests.ps1                      # Configurable PowerShell execution script
└── README.md                          # Full project documentation
```

---

## 4. Setup & Installation

### Prerequisites
- **Python 3.10+** (Tested on Python 3.13)
- **Google Chrome** / **Microsoft Edge** / **Firefox**
- **Git** (optional)

### Step 1: Install Dependencies
Open a command prompt in the project root directory and run:
```bash
pip install -r requirements.txt
```

---

## 5. Test Execution Guide

### Option A: One-Click Execution (Windows)
Double-click `run_tests.bat` or run:
```cmd
run_tests.bat
```
*This executes the full suite in headless mode and automatically opens `reports/report.html` in your default browser.*

### Option B: PowerShell Runner
```powershell
# Run full suite in headless Chrome
.\run_tests.ps1 -Headless

# Run with visible browser window (headed mode)
.\run_tests.ps1

# Run with Microsoft Edge
.\run_tests.ps1 -Browser edge -Headless

# Run only E2E tests
.\run_tests.ps1 -Marker e2e -Headless
```

### Option C: Pytest Direct Commands
```bash
# 1. Run all tests (headless)
python -m pytest --headless

# 2. Run only the End-to-End Purchase Flow
python -m pytest tests/test_e2e_purchase.py --headless

# 3. Run Data-Driven tests from Excel
python -m pytest tests/test_data_driven_excel.py --headless

# 4. Run Data-Driven tests from JSON
python -m pytest tests/test_data_driven_json.py --headless

# 5. Run Cart Operations and Alert tests
python -m pytest tests/test_cart_operations.py --headless

# 6. Run with visible Chrome browser
python -m pytest tests/test_e2e_purchase.py
```

---

## 6. Test Suite Details

### 1. `test_e2e_purchase.py` (End-to-End Purchase Flow)
- **Step 1**: Navigates to application home page and verifies title.
- **Step 2**: Authenticates user via `LoginPage` (with automatic registration if needed).
- **Step 3**: Searches for `MacBook` and verifies matching results.
- **Step 4**: Clicks "Add to Cart" and captures screenshot. Verifies success notification banner.
- **Step 5**: Navigates to Cart and verifies item presence.
- **Step 6**: Updates item quantity from `1` to `2`.
- **Step 7**: Verifies updated quantity = 2, unit price = \$602.00, line total = \$1,204.00 ($602 \times 2$).
- **Step 8**: Dismisses alert popup and verifies total order price ($1,204.00).

### 2. `test_data_driven_excel.py` (Data-Driven via Excel)
- Reads from `test_data/test_data.xlsx` sheet `PurchaseScenarios`.
- Dynamically executes 3 parameterized test cases:
  - `TC_E2E_01`: MacBook (Quantity updated to 2, Total verified: \$1,204.00)
  - `TC_E2E_02`: iPhone (Quantity updated to 3, Total verified: \$369.60)
  - `TC_E2E_03`: Samsung Galaxy Tab 10.1 (Quantity updated to 2, Total verified: \$483.98)

### 3. `test_data_driven_json.py` (Data-Driven via JSON)
- Reads test data from `test_data/test_data.json`.
- Dynamically validates multi-item searches, cart updates, and mathematical assertions.

### 4. `test_cart_operations.py` (Cart Operations & Alerts)
- **Negative Authentication Alert**: Verifies warning banner on invalid credentials.
- **Quantity Update & Alert Dismissal**: Updates item quantity to 4 and tests `AlertHandler` dismissal.
- **Cart Clear State**: Deletes items and verifies the empty cart notification message.

---

## 7. Execution Reports & Evidence

### HTML Report (`reports/report.html`)
The generated report contains:
- **Executive Summary**: Pass/Fail metrics, duration, timestamp.
- **Metadata**: Application URL, Browser, Python version, OS platform, Tester details.
- **Live Logs**: Captured log messages for every individual test step.
- **Embedded Screenshots**: Attached screenshots on failures and step verifications.

### Screenshots (`screenshots/`)
Timestamped PNG files saved automatically during execution:
- `01_home_page_launched_*.png`
- `02_user_logged_in_*.png`
- `03_search_results_*.png`
- `04_product_added_to_cart_*.png`
- `05_cart_initial_view_*.png`
- `06_quantity_updated_*.png`
- `07_cart_verified_alert_dismissed_*.png`
- `excel_TC_*_*.png`
- `json_TC_*_*.png`

### Logs (`logs/automation.log`)
Detailed timestamped logs capturing element locators, clicks, input entries, alerts handled, and mathematical validations:
```
2026-09-27 11:46:58 [INFO] Step 2 passed: User authenticated successfully.
2026-09-27 11:46:58 [INFO] Searching for product: 'MacBook'
2026-09-27 11:46:59 [INFO] Clicked 'Add to Cart' button.
2026-09-27 11:46:59 [INFO] Add to cart alert: 'Success: You have added MacBook to your shopping cart!'
2026-09-27 11:47:00 [INFO] Updating quantity to: 2 for product: 'MacBook'
2026-09-27 11:47:00 [INFO] Verification -> Quantity: 2, Unit Price: $602.0, Line Total: $1204.0
2026-09-27 11:47:01 [INFO] Final Cart Total: $1204.0
2026-09-27 11:47:01 [INFO] ========== E2E Purchase Flow Test COMPLETED SUCCESSFULLY ==========
```

---

## 8. Summary of Achievements

- 🎯 **10/10 Requirements Satisfied**: Complete coverage of all business and technical specifications.
- 🚀 **100% Test Pass Rate**: 10 tests passed across E2E, Excel Data-Driven, JSON Data-Driven, and Regression suites.
- 🛡️ **Zero Flakiness**: Dynamic explicit waits and auto-recovery mechanisms ensure reliable execution in both CI and local desktop environments.
