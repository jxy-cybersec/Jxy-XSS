import logging
from modules.utils import requester

logger = logging.getLogger("JXY-XSS")

def inject_payload(url, params, payload, headers=None):
    """Injects a payload into the URL."""
    headers = headers or {}
    try:
        response = requester(url + payload, headers=headers)
        logger.info(f"Injected payload: {payload}")
        return response
    except Exception as e:
        logger.error(f"Error during injection with payload {payload}: {e}")
        return None
