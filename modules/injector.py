import logging
from modules.utils import requester

logger = logging.getLogger("JXY-XSS")

def inject_payload(url, params, payload, headers=None):
    headers = headers or {}
    logger.info(f"[*] Injecting payload: {payload}")
    try:
        if params:
            for key in params:
                if isinstance(params[key], str):
                    params[key] += payload
                else:
                    logger.error(f"[-] Cannot inject payload into non-string parameter: {key}")
            response = requester(url, params=params, headers=headers)
        else:
            response = requester(url + payload, headers=headers)
        return response
    except Exception as e:
        logger.error(f"[-] Error during injection with payload {payload}: {e}")
        return None
