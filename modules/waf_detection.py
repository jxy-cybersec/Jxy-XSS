import json
import re
from modules.utils import setup_logger, requester

logger = setup_logger(__name__)


def detect_waf(url, headers, payload="<script>alert(1)</script>"):
    """
    Detects if a WAF is present on the target URL.
    Returns the name of the WAF if detected, otherwise None.
    """
    try:
        with open("db/wafSignatures.json") as f:
            waf_signatures = json.load(f)

        logger.info("Checking for WAF...")
        # Updated: Map 'data' to 'params' in requester
        response = requester(url, params={"xss": payload}, headers=headers, method="POST")
        for waf_name, signatures in waf_signatures.items():
            if re.search(signatures["page"], response.text, re.I):
                logger.info(f"WAF detected: {waf_name}")
                return waf_name
        logger.info("No WAF detected.")
        return None
    except Exception as e:
        logger.error(f"Error during WAF detection: {e}")
        return None
