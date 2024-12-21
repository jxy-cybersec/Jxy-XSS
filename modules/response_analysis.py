from fuzzywuzzy import fuzz

def analyze_response(response, payload):
    """
    Validates if the payload is reflected in the response.
    """
    if response and payload.lower() in response.text.lower():
        return True
    return False
