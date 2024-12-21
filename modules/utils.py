import json
import logging
import re
import requests
from urllib.parse import urlparse, urljoin

# Default headers for HTTP requests
default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

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
        print(f"[+] Results saved to: {output_file}")
    except Exception as e:
        print(f"[-] Error saving results to {output_file}: {e}")

def escaped(position, string):
    """
    Determines whether a character at a given position in a string is escaped.

    Args:
        position (int): The position of the character in the string.
        string (str): The string to check.

    Returns:
        bool: True if the character is escaped, False otherwise.
    """
    usable = string[:position][::-1]  # Reverse the string up to the position
    match = re.match(r'\\+', usable)  # Match backslashes
    if match:
        return len(match.group()) % 2 != 0  # Odd number of backslashes means escaped
    return False

def replaceValue(mapping, target_key, new_value, strategy=None):
    """
    Replaces the value of a specific key in a mapping (dictionary) with a new value.

    Args:
        mapping (dict): The dictionary to modify.
        target_key (str): The key whose value is to be replaced.
        new_value (str): The new value to assign to the key.
        strategy (callable, optional): A callable for copying the dictionary, if needed.

    Returns:
        dict: A dictionary with the updated key-value pair.
    """
    another_map = strategy(mapping) if strategy else mapping
    if target_key in another_map:
        another_map[target_key] = new_value
    return another_map

def requester(url, params=None, headers=None, method="GET", timeout=10):
    """
    Sends an HTTP request to the given URL with the specified parameters.

    Args:
        url (str): The target URL.
        params (dict): The request parameters.
        headers (dict): The request headers.
        method (str): The HTTP method ("GET" or "POST").
        timeout (int): The timeout for the request.

    Returns:
        requests.Response: The HTTP response object.
    """
    headers = headers or default_headers
    try:
        if method.upper() == "POST":
            response = requests.post(url, data=params, headers=headers, timeout=timeout)
        else:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        return response
    except requests.RequestException as e:
        print(f"[-] Request failed: {e}")
        return None

def handle_anchor(parent_url, url):
    """
    Handles relative and absolute URLs for anchors or forms.

    Args:
        parent_url (str): The base URL of the page.
        url (str): The URL to process (may be relative or absolute).

    Returns:
        str: The absolute URL.
    """
    if url.startswith("http://") or url.startswith("https://"):
        return url  # Already absolute
    return urljoin(parent_url, url)
