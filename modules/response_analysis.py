import re

def analyze_response(injected_results):
    """
    Analyze responses for signs of successful injection.
    """
    validated_results = []
    print("[*] Validating responses to ensure actual XSS execution...")
    for param, payload, response_text in injected_results:
        # Check if payload is reflected in the response text
        if payload in response_text:
            # Additional verification for HTML context
            if "<script>" in response_text or re.search(r"<.*on\w+=.*>", response_text):
                print(f"[+] Verified XSS: Parameter '{param}' with payload: {payload}")
                validated_results.append((param, payload))
            else:
                print(f"[-] False positive ignored for: {param} with payload: {payload}")
        else:
            print(f"[-] Payload not reflected for: {param} with payload: {payload}")
    return validated_results
