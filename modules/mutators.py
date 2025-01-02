import urllib.parse

def encode_payload(payload):
    """
    Encode the payload with URL encoding.
    """
    return urllib.parse.quote(payload)

def double_encode_payload(payload):
    """
    Encode the payload twice with URL encoding.
    """
    return urllib.parse.quote(urllib.parse.quote(payload))

def html_entity_encode(payload):
    """
    Encode the payload with HTML entities.
    """
    encoded = ""
    for char in payload:
        encoded += f"&#{ord(char)};"
    return encoded

def javascript_escape(payload):
    """
    Escape the payload for JavaScript injection.
    """
    escaped = payload.replace("\\", "\\\\").replace("\"", "\\\"").replace("'", "\\'")
    return escaped

def recursive_mutations(payload):
    """
    Generate slight variations for recursive testing.
    """
    variations = [payload[::-1], payload.upper(), payload.lower()]
    return [encode_payload(var) for var in variations]

def generate_mutations(payload):
    """
    Generate multiple mutations of the given payload for testing.
    """
    return {
        "original": payload,
        "url_encoded": encode_payload(payload),
        "double_url_encoded": double_encode_payload(payload),
        "html_entity_encoded": html_entity_encode(payload),
        "javascript_escaped": javascript_escape(payload),
    }
