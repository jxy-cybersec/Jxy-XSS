def analyze_response(response, payload):
    """
    Analyzes the response to check for payload reflection.
    Args:
        response (requests.Response): The HTTP response object.
        payload (str): The injected payload.
    Returns:
        bool: True if the payload is reflected, False otherwise.
    """
    if payload in response.text:
        print(f"[+] Payload reflected: {payload}")
        return True
    return False
