def analyze_response(response, payload):
    """
    Analyze the HTTP response for XSS reflections.
    """
    if response and payload in response.text:
        return True
    return False
