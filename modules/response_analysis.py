def analyze_response(injected_results):
    """
    Analyze responses for signs of successful injection.
    """
    for param, payload, response_text in injected_results:
        if payload in response_text:
            print(f"[+] Vulnerable parameter found: {param} with payload: {payload}")
        else:
            print(f"[-] No XSS detected for parameter: {param} with payload: {payload}")
