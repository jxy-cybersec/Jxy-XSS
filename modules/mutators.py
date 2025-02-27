import urllib.parse

def encode_payload(payload):
    """Encode the payload with URL encoding."""
    return urllib.parse.quote(payload)

def double_encode_payload(payload):
    """Encode the payload twice with URL encoding."""
    return urllib.parse.quote(urllib.parse.quote(payload))

def html_entity_encode(payload):
    """Encode the payload with HTML entities."""
    return "".join(f"&#{ord(char)};" for char in payload)

def javascript_escape(payload):
    """Escape the payload for JavaScript injection."""
    return payload.replace("\\", "\\\\").replace("\"", "\\\"").replace("'", "\\'")

def generate_mutations(payload):
    """Generate multiple mutations of the payload."""
    return {
        "original": payload,
        "url_encoded": encode_payload(payload),
        "double_url_encoded": double_encode_payload(payload),
        "html_entity_encoded": html_entity_encode(payload),
        "javascript_escaped": javascript_escape(payload),
    }
