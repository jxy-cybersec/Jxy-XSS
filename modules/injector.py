import requests

def inject_payload(url, params, payload, method="GET"):
    """
    Inject payloads into parameters for testing XSS vulnerabilities.
    """
    injected_results = []
    for param in params:
        test_params = params.copy()
        test_params[param] = payload  # Inject the payload into the current parameter

        try:
            if method.upper() == "GET":
                response = requests.get(url, params=test_params)
            elif method.upper() == "POST":
                response = requests.post(url, data=test_params)
            else:
                print(f"[!] Unsupported HTTP method: {method}")
                continue

            # Append results for analysis
            injected_results.append((param, payload, response.text))

        except requests.RequestException as e:
            print(f"[!] Error injecting payload into {url}: {e}")

    return injected_results
