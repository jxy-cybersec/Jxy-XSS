import json
import re
from modules.utils import requester, setup_logger

logger = setup_logger()


def detect_waf(url, headers, payload="<script>alert(1)</script>"):
    """
    Detects if a WAF is present on the target URL.
    Returns the name of the WAF if detected, otherwise None.
    """
    try:
        with open("db/wafSignatures.json") as f:
            waf_signatures = json.load(f)

        logger.info("Checking for WAF...")
        response = requester(url, data={"xss": payload}, headers=headers, method="POST")
        if not response:
            logger.error("Failed to get a response from the server.")
            return None

        for waf_name, signatures in waf_signatures.items():
            if re.search(signatures["page"], response.text, re.I):
                logger.info(f"WAF detected: {waf_name}")
                return waf_name

        logger.info("No WAF detected.")
        return None
    except FileNotFoundError:
        logger.error("WAF signature database not found. Skipping WAF detection.")
        return None
    except Exception as e:
        logger.error(f"Error during WAF detection: {e}")
        return None
