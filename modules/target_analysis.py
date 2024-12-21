from modules.htmlParser import htmlParser
from modules.dom import dom_check

def analyze_target(response):
    """
    Analyzes the target response for vulnerabilities.

    Args:
        response (obj): HTTP response object.

    Returns:
        dict: Combined results from HTML and DOM analysis.
    """
    html_contexts = htmlParser(response.text)
    dom_vulnerabilities = dom_check(response.text)
    return {
        "html_contexts": html_contexts,
        "dom_vulnerabilities": dom_vulnerabilities
    }
