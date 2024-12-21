from fuzzywuzzy import fuzz
from modules.dom import dom_check
from modules.colors import green, red, end

def analyze_response(response, payload):
    """
    Validates if the payload is reflected in the response.

    Args:
        response (obj): HTTP response object.
        payload (str): Payload used in the request.

    Returns:
        bool: True if reflection is detected, False otherwise.
    """
    if not response or not response.text:
        return False

    reflections = response.text.lower().count(payload.lower())
    if reflections > 0:
        print(f"{green}[+] Reflection detected: {payload}{end}")
        return True
    return False

def analyze_dom(response):
    """
    Analyzes DOM for vulnerabilities using source-sink relationships.

    Args:
        response (str): The HTML response as a string.

    Returns:
        list: List of detected vulnerabilities, if any.
    """
    vulnerabilities = dom_check(response)
    if vulnerabilities:
        print(f"{red}[!] DOM vulnerabilities detected!{end}")
        for vulnerability in vulnerabilities:
            print(vulnerability)
    return vulnerabilities
