import json
import re
from modules.utils import setup_logger, requester

logger = setup_logger()

def detect_waf(url, headers=None, payload="<script>alert(1)</script>"):
    """
    Detects if a WAF is present on the target URL.

    Args:
        url (str): The target URL.
        headers (dict, optional): HTTP headers.
        payload (str): The payload to test for WAF detection.

    Returns:
        str or None: Name of the detected WAF, or None if no WAF is detected.
    """
    try:
        with open("db/wafSignatures.json") as f:
            waf_signatures = json.load(f)

        logger.info("Checking for WAF...")
        response = requester(url, data={"xss": payload}, headers=headers)
        if not response:
            return None

        for waf_name, signatures in waf_signatures.items():
            if re.search(signatures["page"], response.text, re.I):
                logger.info(f"WAF detected: {waf_name}")
                return waf_name

        logger.info("No WAF detected.")
        return None
    except Exception as e:
        logger.error(f"Error during WAF detection: {e}")
        return None
