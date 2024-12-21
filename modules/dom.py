import re
from modules.utils import setup_logger
from modules.colors import yellow, red, green, end

def dom_check(response):
    """
    Checks for DOM-based XSS by analyzing source-sink relationships in JavaScript.

    Args:
        response (str): The HTML response as a string.

    Returns:
        list: A list of highlighted scripts with potential vulnerabilities.
    """
    logger = setup_logger()
    if not response:
        logger.warning(f"{yellow}[!] Empty response provided for DOM check.{end}")
        return []

    logger.info(f"{green}[+] Starting DOM-based XSS check...{end}")
    sources = r'\b(?:document\.(URL|documentURI|cookie|referrer)|location\.(href|search|hash)|window\.name)\b'
    sinks = r'\b(?:eval|innerHTML|document\.write|setTimeout|Function)\b'
    scripts = re.findall(r'(?i)(?s)<script[^>]*>(.*?)</script>', response)
    highlighted = []

    for script in scripts:
        source_matches = re.findall(sources, script)
        sink_matches = re.findall(sinks, script)
        if source_matches or sink_matches:
            for source in source_matches:
                script = script.replace(source, f"{yellow}{source}{end}")
            for sink in sink_matches:
                script = script.replace(sink, f"{red}{sink}{end}")
            highlighted.append(script)
    if highlighted:
        logger.info(f"{green}[+] Detected potential DOM-based vulnerabilities.{end}")
    else:
        logger.info(f"{yellow}[!] No DOM-based vulnerabilities found.{end}")
    return highlighted
