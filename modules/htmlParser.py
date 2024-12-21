import re

def htmlParser(response):
    """
    Parses HTML for potential injection points.
    """
    xsschecker = "xsscheck"
    contexts = {}
    response = re.sub(r'<!--.*?-->', '', response, flags=re.S)

    scripts = re.finditer(r'(?i)<script.*?>.*?</script>', response, re.S)
    for script in scripts:
        contexts[script.start()] = {"context": "script", "details": {"content": script.group()}}

    attributes = re.finditer(r'<[^>]*?%s[^>]*?>' % xsschecker, response, re.S)
    for attr in attributes:
        contexts[attr.start()] = {"context": "attribute", "details": {"tag": attr.group()}}

    return contexts
