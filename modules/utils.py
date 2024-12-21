import json
import logging
import re
import requests
from urllib.parse import urljoin, urlparse


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

    if not logger.handlers:
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
    """
    try:
        with open(output_file, "w") as file:
            json.dump(results, file, indent=4)
        print(f"[+] Results saved to: {output_file}")
    except Exception as e:
        print(f"[-] Error saving results to {output_file}: {e}")


def handle_anchor(base_url, relative_url):
    """
    Resolves relative or partial URLs into absolute URLs.

    Args:
        base_url (str): The base URL (e.g., the page being crawled).
        relative_url (str): The relative or incomplete URL.

    Returns:
        str: The resolved absolute URL.
    """
    if not relative_url:
        return base_url
    return urljoin(base_url, relative_url)


def requester(url, params=None, headers=None, method="GET", timeout=10):
    """
    Makes an HTTP request to the given URL.

    Args:
        url (str): The target URL.
        params (dict, optional): Query or form parameters.
        headers (dict, optional): HTTP headers.
        method (str): HTTP method (GET or POST).
        timeout (int): Timeout for the request.

    Returns:
        obj: Response object.
    """
    try:
        if method.upper() == "POST":
            return requests.post(url, data=params, headers=headers, timeout=timeout)
        return requests.get(url, params=params, headers=headers, timeout=timeout)
    except Exception as e:
        print(f"[-] Error making request to {url}: {e}")
        return None


def replaceValue(mapping, key, new_value, strategy=None):
    """
    Replace a specific key's value in a dictionary.

    Args:
        mapping (dict): The dictionary to modify.
        key (str): Key whose value should be replaced.
        new_value (str): The new value.
        strategy (function, optional): Function for copying (e.g., `copy.deepcopy`).

    Returns:
        dict: Updated dictionary.
    """
    another_map = strategy(mapping) if strategy else mapping
    if key in another_map:
        another_map[key] = new_value
    return another_map


def escaped(position, string):
    """
    Determines if a character at a position is escaped.

    Args:
        position (int): Position of the character.
        string (str): The string to check.

    Returns:
        bool: True if escaped, False otherwise.
    """
    usable = string[:position][::-1]
    match = re.match(r'\\+', usable)
    if match:
        return len(match.group()) % 2 != 0
    return False
