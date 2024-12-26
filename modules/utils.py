import logging
import subprocess
import time
import requests

def setup_logger():
    """Sets up a logger for the tool."""
    logger = logging.getLogger("JXY-XSS")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s]: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

def save_results(file_path, results):
    """Saves scan results to a file."""
    try:
        with open(file_path, 'w') as f:
            for result in results:
                f.write(result + "\n")
    except Exception as e:
        logger = setup_logger()
        logger.error(f"Failed to save results to {file_path}: {e}")

def rate_limit(requests_per_second):
    """Implements rate limiting for requests."""
    delay = 1.0 / requests_per_second
    time.sleep(delay)

def requester(url, method="GET", params=None, data=None, headers=None):
    """Handles HTTP requests."""
    try:
        if method == "GET":
            return requests.get(url, params=params, headers=headers, timeout=10)
        elif method == "POST":
            return requests.post(url, data=data, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        logger = setup_logger()
        logger.error(f"Request error: {e}")
        return None

def update_tool(logger):
    """Updates the tool to the latest version using Git."""
    logger.info("Checking for updates...")
    try:
        result = subprocess.run(
            ["git", "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "Already up to date." in result.stdout:
            logger.info("The tool is already up to date.")
        else:
            logger.info("Tool successfully updated.")
    except FileNotFoundError:
        logger.error("Git is not installed. Please install Git to use the update feature.")
    except Exception as e:
        logger.error(f"An error occurred while updating: {e}")
