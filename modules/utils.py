import requests
import logging
import time

logger = logging.getLogger("JXY-XSS")

def rate_limiter(max_requests_per_second):
    """
    Decorator to limit the rate of requests.
    """
    min_interval = 1 / max_requests_per_second

    def decorator(func):
        last_call = [0]

        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator

@rate_limiter(10)  # Limit to 10 requests per second
def requester(url, params=None, headers=None, method="GET", timeout=10):
    """
    Sends an HTTP request.

    Args:
        url (str): Target URL.
        params (dict): Query parameters for the request.
        headers (dict): Headers for the request.
        method (str): HTTP method (GET or POST).
        timeout (int): Timeout for the request.

    Returns:
        Response: The HTTP response object.
    """
    headers = headers or {}
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, data=params, headers=headers, timeout=timeout)
        else:
            logger.error(f"[-] Unsupported HTTP method: {method}")
            return None
        logger.info(f"[+] Received response with status code: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"[-] Request error: {e}")
        return None

def setup_logger(log_file="tool.log"):
    """
    Sets up the logger for the tool.

    Args:
        log_file (str): File to store logs.
    """
    logger = logging.getLogger("JXY-XSS")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s]: %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger