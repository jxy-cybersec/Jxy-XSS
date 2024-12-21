from modules.htmlParser import htmlParser
from modules.dom import dom_check
from modules.utils import setup_logger

logger = setup_logger()

def analyze_target(response_text):
    """
    Analyzes the target response for vulnerabilities.
    """
    if not response_text.strip():
        logger.warning("[!] Empty response provided for DOM check.")
        return {
            "html_contexts": {},
            "dom_vulnerabilities": []
        }

    html_contexts = htmlParser(response_text)
    dom_vulnerabilities = dom_check(response_text)
    return {
        "html_contexts": html_contexts,
        "dom_vulnerabilities": dom_vulnerabilities
    }
