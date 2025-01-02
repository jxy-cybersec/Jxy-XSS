import logging
from modules.utils import requester
from modules.mutators import recursive_mutations

logger = logging.getLogger("JXY-XSS")

def inject_payload(url, params, payload, headers=None, refine=True):
    """
    Injects payloads with optional recursive refinement.

    Args:
        url (str): Target URL.
        params (dict): Parameters to inject the payload into.
        payload (str): Payload to inject.
        headers (dict): Additional headers for the request.
        refine (bool): Whether to perform recursive testing on successful payloads.

    Returns:
        Response: The HTTP response object.
    """
    headers = headers or {}
    logger.info(f"[*] Injecting payload: {payload}")

    try:
        if params:
            for key in params.keys():
                original_value = params[key]
                if isinstance(original_value, str):
                    params[key] = original_value + payload
                else:
                    logger.error(f"[-] Cannot inject payload into non-string parameter: {key}")
            response = requester(url, params=params, headers=headers)
        else:
            response = requester(url + payload, headers=headers)

        # Perform recursive testing if response indicates success
        if refine and response and payload in response.text:
            logger.info(f"[+] Refining payload: {payload}")
            refined_payloads = recursive_mutations(payload)
            for refined_payload in refined_payloads:
                inject_payload(url, params, refined_payload, headers, refine=False)

        return response
    except Exception as e:
        logger.error(f"[-] Error during injection with payload {payload}: {e}")
        return None
