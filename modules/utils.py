import requests
import logging

logger = logging.getLogger("JXY-XSS")

def requester(url, params=None, headers=None, method="GET", timeout=10):
    """Send an HTTP request."""
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, data=params, headers=headers, timeout=timeout)
        else:
            logger.error(f"Unsupported HTTP method: {method}")
            return None
        logger.info(f"Received response with status code: {response.status_code}")
        return response
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return None

def setup_logger(log_file="tool.log"):
    """
    Sets up the logger for the tool.

    Args:
        log_file (str): File to store logs.
    """
    logger = logging.getLogger("JXY-XSS")
    if not logger.hasHandlers():  # Avoid duplicate handlers
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s]: %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger

def update_tool():
    """Update the tool using Git."""
    import subprocess
    try:
        subprocess.run(["git", "pull"], check=True)
        logger.info("Tool successfully updated!")
    except Exception as e:
        logger.error(f"Failed to update tool: {e}")
