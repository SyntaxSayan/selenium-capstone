import os
import configparser

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE_PATH = os.path.join(PROJECT_ROOT, "config", "config.ini")

class ConfigReader:
    """Utility class to read configurations from config.ini."""

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    @classmethod
    def get_base_url(cls):
        return cls.config.get("common_info", "base_url", fallback="https://tutorialsninja.com/demo/")

    @classmethod
    def get_browser(cls):
        return cls.config.get("common_info", "browser", fallback="chrome")

    @classmethod
    def get_headless(cls):
        return cls.config.getboolean("common_info", "headless", fallback=False)

    @classmethod
    def get_implicit_wait(cls):
        return cls.config.getint("common_info", "implicit_wait", fallback=10)

    @classmethod
    def get_explicit_wait(cls):
        return cls.config.getint("common_info", "explicit_wait", fallback=15)

    @classmethod
    def get_page_load_timeout(cls):
        return cls.config.getint("common_info", "page_load_timeout", fallback=30)

    @classmethod
    def get_valid_email(cls):
        return cls.config.get("credentials", "valid_email", fallback="tester_capstone_selenium@gmail.com")

    @classmethod
    def get_valid_password(cls):
        return cls.config.get("credentials", "valid_password", fallback="Password@123")

    @classmethod
    def get_user_firstname(cls):
        return cls.config.get("credentials", "user_firstname", fallback="Capstone")

    @classmethod
    def get_user_lastname(cls):
        return cls.config.get("credentials", "user_lastname", fallback="Tester")

    @classmethod
    def get_user_telephone(cls):
        return cls.config.get("credentials", "user_telephone", fallback="9876543210")

    @classmethod
    def get_invalid_email(cls):
        return cls.config.get("credentials", "invalid_email", fallback="invalid_user_xyz@test.com")

    @classmethod
    def get_invalid_password(cls):
        return cls.config.get("credentials", "invalid_password", fallback="WrongPassword999")

    @classmethod
    def get_excel_data_path(cls):
        rel_path = cls.config.get("paths", "excel_data_path", fallback="test_data/test_data.xlsx")
        return os.path.join(PROJECT_ROOT, rel_path)

    @classmethod
    def get_json_data_path(cls):
        rel_path = cls.config.get("paths", "json_data_path", fallback="test_data/test_data.json")
        return os.path.join(PROJECT_ROOT, rel_path)

    @classmethod
    def get_screenshot_dir(cls):
        rel_path = cls.config.get("paths", "screenshot_dir", fallback="screenshots")
        path = os.path.join(PROJECT_ROOT, rel_path)
        os.makedirs(path, exist_ok=True)
        return path

    @classmethod
    def get_report_dir(cls):
        rel_path = cls.config.get("paths", "report_dir", fallback="reports")
        path = os.path.join(PROJECT_ROOT, rel_path)
        os.makedirs(path, exist_ok=True)
        return path

    @classmethod
    def get_log_file_path(cls):
        rel_path = cls.config.get("paths", "log_file", fallback="logs/automation.log")
        path = os.path.join(PROJECT_ROOT, rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path
