def analyze_response(response, payload):
    """Analyze the response to detect XSS vulnerabilities."""
    if payload in response.text:
        return {"vulnerable": True, "type": "Reflected XSS", "details": f"Payload reflected in response: {payload}"}
    return {"vulnerable": False}
