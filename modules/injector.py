import copy
import time
from modules.utils import requester
from modules.response_analysis import analyze_response
from modules.mutators import mutate_payload

def inject_payload(url, params, payload, headers=None, method="GET", rate_limit=0.1):
    """
    Injects payloads into the target URL and analyzes the response.
    Args:
        url (str): Target URL.
        params (dict): Parameters for injection.
        payload (str): The payload to inject.
        headers (dict): HTTP headers.
        method (str): HTTP method (GET/POST).
        rate_limit (float): Time delay between requests (in seconds).
    Returns:
        bool: True if the injection was successful, False otherwise.
    """
    for mutation in mutate_payload(payload):
        modified_params = copy.deepcopy(params)
        for key in modified_params.keys():
            modified_params[key] = mutation
        time.sleep(rate_limit)  # Rate limiting
        try:
            response = requester(url, params=modified_params, headers=headers, method=method)
            if analyze_response(response, mutation):
                print(f"[+] Reflection detected: {mutation}")
                return True
        except Exception as e:
            print(f"[-] Error during injection with payload {mutation}: {e}")
    return False
