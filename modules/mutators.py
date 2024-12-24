import urllib.parse
import base64

def url_encode(payload):
    """Encodes the payload using URL encoding."""
    return urllib.parse.quote(payload)

def base64_encode(payload):
    """Encodes the payload in Base64."""
    return base64.b64encode(payload.encode()).decode()

def escape_html(payload):
    """Escapes special HTML characters."""
    return payload.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;").replace("\"", "&quot;")

def mutate_payload(payload):
    """Generates multiple variations of the payload using different encoding techniques."""
    return [
        payload,
        url_encode(payload),
        base64_encode(payload),
        escape_html(payload),
    ]
