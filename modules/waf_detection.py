import requests
import logging

logger = logging.getLogger("JXY-XSS")

def detect_waf(url):
    """
    Detects if a WAF is present at the target URL.

    Args:
        url (str): The target URL.

    Returns:
        str: The name of the detected WAF, or None if no WAF is detected.
    """
    try:
        response = requests.get(url, timeout=5)
        waf_signatures = {
            "Cloudflare": {"headers": "cf-ray"},
            "AWS WAF": {"headers": "aws-waf"},
            "Imperva SecureSphere": {"headers": "x-iinfo"},
        }

        for waf_name, signature in waf_signatures.items():
            if signature.get("headers") in response.headers:
                logger.info(f"[+] Detected WAF: {waf_name}")
                return waf_name
        logger.info("[!] No WAF detected.")
        return None
    except requests.RequestException as e:
        logger.error(f"[-] WAF detection error: {e}")
        return None
