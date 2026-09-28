import json
import os
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("JsonUtil")

class JsonUtil:
    """Utility class to read test data from JSON files."""

    @staticmethod
    def read_json(file_path):
        """Reads a JSON file and returns parsed Python object."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Loaded JSON data from {file_path}")
            return data
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            raise

    @staticmethod
    def get_test_cases(file_path, key="test_cases"):
        """Reads a specific array of test cases from JSON."""
        data = JsonUtil.read_json(file_path)
        return data.get(key, [])
