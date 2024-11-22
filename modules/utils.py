import logging
import json

class CustomFormatter(logging.Formatter):
    """
    Custom logging formatter to add colors based on log level.
    """
    green = "\033[92m"
    yellow = "\033[93m"
    reset = "\033[0m"
    format = "[%(asctime)s] [JXY-XSS] [%(levelname)s]: %(message)s"

    FORMATS = {
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: "\033[91m" + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.format)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger():
    """
    Sets up the logger for JXY-XSS.
    """
    logger = logging.getLogger("JXY-XSS")
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def save_results(file_path, results):
    """
    Saves the scan results to a file in JSON format.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)
        print(f"[+] Results saved to {file_path}")
    except IOError as e:
        print(f"[!] Failed to save results: {e}")
