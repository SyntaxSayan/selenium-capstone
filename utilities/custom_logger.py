import logging
import os
import sys
from config.config_reader import ConfigReader

class CustomLogger:
    """Provides a standardized logger instance for the automation framework."""

    @staticmethod
    def get_logger(name="AutomationFramework"):
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            log_file = ConfigReader.get_log_file_path()
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

            # Formatter
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # File Handler
            file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # Console Handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger
