def analyze_response(response, payload):
    """
    Analyze the response to detect if the payload is reflected.

    Args:
        response (Response): HTTP response object.
        payload (str): The payload used for testing.

    Returns:
        bool: True if the payload is reflected, False otherwise.
    """
    if response and payload in response.text:
        return True
    return False
