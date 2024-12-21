import json
import logging
import requests


def setup_logger(log_file="tool.log", log_level=logging.INFO):
    """
    Sets up a logger to write to both the console and a log file.
    """
    logger = logging.getLogger("JXY-XSS")
    logger.setLevel(log_level)

    if not logger.hasHandlers():
        formatter = logging.Formatter(
            "%(asctime)s [%(name)s] [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()


def requester(url, params=None, headers=None, data=None, method="GET", timeout=10):
    """
    Sends an HTTP request to the given URL.
    Supports both GET and POST requests.
    """
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, data=data, headers=headers, timeout=timeout)
        else:
            logger.error(f"Unsupported HTTP method: {method}")
            return None
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None


def save_results(output_file, results):
    """
    Saves the scan results to a file in JSON format.

    Args:
        output_file (str): Path to the output file.
        results (list): List of dictionaries containing scan results.

    Returns:
        None
    """
    try:
        with open(output_file, "w") as file:
            json.dump(results, file, indent=4)
        logger.info(f"Results saved to: {output_file}")
    except Exception as e:
        logger.error(f"Error saving results to {output_file}: {e}")
