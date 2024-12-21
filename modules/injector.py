import copy
import time
from modules.utils import requester, setup_logger
from modules.response_analysis import analyze_response

logger = setup_logger()

REQUEST_TIMEOUT = 10  # Set a timeout for requests
RATE_LIMIT = 0.2  # Rate limit (5 requests/s)


def inject_payload(url, params, payload, headers=None, method="GET"):
    """
    Injects a payload into the specified parameters and sends the request.

    Args:
        url (str): The target URL.
        params (dict): The parameters for the request.
        payload (str): The payload to inject.
        headers (dict): Optional headers for the request.
        method (str): HTTP method ("GET" or "POST").

    Returns:
        response: The server's response if successful, None otherwise.
    """
    try:
        def inject_recursive(target):
            """
            Recursively inject payloads into nested parameters.
            """
            if isinstance(target, dict):
                for key in target.keys():
                    target[key] = inject_recursive(target[key])
            elif isinstance(target, list):
                target = [inject_recursive(item) for item in target]
            elif isinstance(target, str):
                target += payload
            else:
                target = str(target) + payload
            return target

        # Create a modified copy of the parameters
        modified_params = copy.deepcopy(params)
        modified_params = inject_recursive(modified_params)

        # Send the request
        time.sleep(RATE_LIMIT)  # Rate limit: 5 requests per second
        response = requester(url, params=modified_params, headers=headers, method=method, timeout=REQUEST_TIMEOUT)

        # Analyze the response for the payload
        if analyze_response(response, payload):
            return response
    except Exception as e:
        logger.error(f"Error during injection with payload {payload}: {e}")
    return None
