import os
from datetime import datetime
from config.config_reader import ConfigReader

class ScreenshotUtil:
    """Helper utility for capturing and storing screenshots."""

    @staticmethod
    def capture_screenshot(driver, step_name="step"):
        """Captures a screenshot with timestamp and returns absolute path."""
        try:
            folder = ConfigReader.get_screenshot_dir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
            sanitized_name = "".join([c if c.isalnum() or c in ("-", "_") else "_" for c in step_name])
            filename = f"{sanitized_name}_{timestamp}.png"
            filepath = os.path.join(folder, filename)
            driver.save_screenshot(filepath)
            return filepath
        except Exception as e:
            print(f"[ScreenshotUtil] Failed to take screenshot: {e}")
            return None
