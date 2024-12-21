import copy
from modules.utils import replaceValue, requester
from modules.response_analysis import analyze_response
from modules.colors import red, green, end
from modules.utils import setup_logger

logger = setup_logger()

def inject_payload(url, params, payload, headers=None, method="GET"):
    """
    Injects a payload into the specified parameters and sends the request.

    Args:
        url (str): The target URL.
        params (dict): Dictionary of parameters to inject.
        payload (str): The payload to test.
        headers (dict, optional): HTTP headers for the request.
        method (str): HTTP method to use (GET or POST).

    Returns:
        list: List of injection results.
    """
    try:
        results = []

        if not isinstance(params, dict):
            logger.error(f"{red}[-] Invalid params structure. Expected dict but got {type(params).__name__}.{end}")
            return []

        for param, value in params.items():
            # Replace the current parameter's value with the payload
            modified_params = replaceValue(params, param, payload, copy.deepcopy)
            
            # Make the request with the injected payload
            response = requester(url, params=modified_params, headers=headers, method=method)
            
            # Analyze the response
            if response and analyze_response(response, payload):
                results.append({
                    "url": url,
                    "param": param,
                    "payload": payload,
                    "response": response.text
                })
                logger.info(f"{green}[+] Injection successful on parameter: {param}{end}")
            else:
                logger.info(f"{red}[-] Injection failed on parameter: {param}{end}")

        return results
    except Exception as e:
        logger.error(f"{red}[-] Error during injection: {e}{end}")
        return []
