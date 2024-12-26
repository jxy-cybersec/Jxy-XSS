import urllib.parse

def encode_payload(payload):
    return urllib.parse.quote(payload)

def double_encode_payload(payload):
    return urllib.parse.quote(urllib.parse.quote(payload))

def html_entity_encode(payload):
    return "".join(f"&#{ord(char)};" for char in payload)

def generate_mutations(payload):
    return {
        "original": payload,
        "url_encoded": encode_payload(payload),
        "double_url_encoded": double_encode_payload(payload),
        "html_entity_encoded": html_entity_encode(payload),
    }
