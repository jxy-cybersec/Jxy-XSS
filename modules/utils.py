import logging
import requests

logger = logging.getLogger("JXY-XSS")

def requester(url, params=None, headers=None, method="GET", timeout=10):
    headers = headers or {}
    try:
        if method.upper() == "GET":
            return requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            return requests.post(url, data=params, headers=headers, timeout=timeout)
        else:
            logger.error(f"Unsupported method: {method}")
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
    return None

def setup_logger(log_file="tool.log"):
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
