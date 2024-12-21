import re
from modules.utils import setup_logger
from modules.colors import yellow, red, end

def dom_check(response):
    """
    Checks for DOM-based XSS by analyzing source-sink relationships in JavaScript.
    """
    logger = setup_logger()
    sources = r'\b(?:document\.(URL|documentURI|cookie|referrer)|location\.(href|search|hash)|window\.name)\b'
    sinks = r'\b(?:eval|innerHTML|document\.write|setTimeout|Function)\b'
    scripts = re.findall(r'(?i)(?s)<script[^>]*>(.*?)</script>', response)
    highlighted = []

    for script in scripts:
        source_matches = re.findall(sources, script)
        sink_matches = re.findall(sinks, script)

        if source_matches or sink_matches:
            for source in source_matches:
                # Handle tuple case for regex groups
                source = ''.join(source) if isinstance(source, tuple) else source
                script = script.replace(source, f"{yellow}{source}{end}")
            for sink in sink_matches:
                script = script.replace(sink, f"{red}{sink}{end}")
            highlighted.append(script)

    if not highlighted:
        logger.info("[+] No DOM-based XSS vulnerabilities found.")
    return highlighted
