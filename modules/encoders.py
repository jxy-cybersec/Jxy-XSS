import base64

def base64_encode(string):
    """
    Encodes the given string to Base64.
    """
    return base64.b64encode(string.encode()).decode()

def base64_decode(string):
    """
    Decodes the given Base64 string.
    """
    try:
        return base64.b64decode(string).decode()
    except Exception:
        return None
