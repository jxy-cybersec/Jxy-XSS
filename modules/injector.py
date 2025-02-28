import logging
from modules.utils import requester
from modules.analysis import validate_response
from termcolor import colored

logger = logging.getLogger("JXY-XSS")

def inject_payload(url, params, payload, headers=None):
    """Injects a payload and verifies execution."""
    headers = headers or {}

    try:
        response = requester(url + payload, headers=headers)
        logger.info(colored(f"Injected payload: {payload}", "cyan"))

        # Validate execution
        result = validate_response(response, payload)

        if result["vulnerable"]:
            logger.info(colored(f"✅ Vulnerable to {result['type']} with payload: {payload}", "green"))
        else:
            logger.info(colored(f"❌ Payload did not execute: {payload}", "red"))

        return response
    except Exception as e:
        logger.error(colored(f"[-] Error injecting payload {payload}: {e}", "red"))
        return None
