from modules.htmlParser import htmlParser
from modules.dom import dom_check

def analyze_target(response_text):
    """
    Analyzes the target response for vulnerabilities.
    Args:
        response_text (str): The raw HTML content of the response.

    Returns:
        dict: A dictionary containing HTML contexts and DOM vulnerabilities.
    """
    # Pass the raw text directly to htmlParser
    html_contexts = htmlParser(response_text)
    dom_vulnerabilities = dom_check(response_text)  # Ensure this also handles raw strings

    return {
        "html_contexts": html_contexts,
        "dom_vulnerabilities": dom_vulnerabilities
    }
