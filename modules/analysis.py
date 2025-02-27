def validate_response(response, payload):
    """
    Validates if the injected payload reflects or executes in the response.

    Args:
        response (Response): The HTTP response object.
        payload (str): The injected payload.

    Returns:
        bool: True if the payload reflects or executes, False otherwise.
    """
    if payload in response.text:
        return True

    # Check if the payload is stored in headers
    if any(payload in value for value in response.headers.values()):
        return True

    return False
