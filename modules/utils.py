import logging
import time
import requests

def setup_logger(log_file="tool.log", log_level=logging.INFO):
    """
    Sets up a logger to write to both the console and a log file.
    """
    logger = logging.getLogger("JXY-XSS")
    logger.setLevel(log_level)

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

def requester(url, params=None, headers=None, method="GET", timeout=10, retries=3):
    """
    Sends an HTTP request with retry logic.

    Args:
        url (str): Target URL.
        params (dict): Parameters to send in the query string.
        headers (dict): HTTP headers.
        method (str): HTTP method (GET or POST).
        timeout (int): Timeout for requests in seconds.
        retries (int): Number of retries for failed requests.

    Returns:
        Response: HTTP response object or None if all retries fail.
    """
    for attempt in range(retries):
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, data=params, headers=headers, timeout=timeout)
            else:
                raise ValueError("Unsupported HTTP method.")
            
            # Return response if status code is 200
            if response.status_code == 200:
                return response
            else:
                print(f"[-] Received HTTP {response.status_code} for {url}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error during request to {url}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print("[-] Max retries exceeded.")
    return None
