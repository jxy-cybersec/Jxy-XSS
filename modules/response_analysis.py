def analyze_response(response, payload):
    """
    Analyzes the response to check if the payload is reflected.

    Args:
        response (Response): The HTTP response object.
        payload (str): The payload to look for in the response.

    Returns:
        bool: True if the payload is reflected in the response, False otherwise.
    """
    if response and payload in response.text:
        return True
    return False
