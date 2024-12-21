from modules.htmlParser import htmlParser

def analyze_target(response):
    """
    Analyzes the target response for vulnerabilities.
    """
    html_contexts = htmlParser(response)
    return {
        "html_contexts": html_contexts
    }
