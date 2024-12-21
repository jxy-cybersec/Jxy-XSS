import copy
from modules.utils import replaceValue, requester
from modules.response_analysis import analyze_response

def inject_payload(url, params, payload, headers=None, method="GET"):
    """
    Injects a payload into the specified parameters and sends the request.

    Args:
        url (str): Target URL.
        params (dict): Query or form parameters to inject.
        payload (str): The payload to inject.
        headers (dict, optional): Additional headers.
        method (str): HTTP method (GET or POST).

    Returns:
        dict or None: Response data if successful, otherwise None.
    """
    try:
        for param in params:
            modified_params = replaceValue(params, param, payload, copy.deepcopy)
            response = requester(url, params=modified_params, headers=headers, method=method)
            if analyze_response(response, payload):
                return {
                    "url": url,
                    "params": params,
                    "payload": payload,
                    "response": response.text
                }
    except Exception as e:
        print(f"[-] Error during injection: {e}")
    return None
