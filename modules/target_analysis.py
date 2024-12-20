from modules.htmlParser import htmlParser
from modules.dom import dom_check

def analyze_target(response):
    """
    Analyzes the target response for vulnerabilities.
    """
    html_contexts = htmlParser(response)
    dom_vulnerabilities = dom_check(response.text)
    return {
        "html_contexts": html_contexts,
        "dom_vulnerabilities": dom_vulnerabilities
    }
