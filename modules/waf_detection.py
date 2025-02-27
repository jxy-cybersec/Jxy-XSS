import requests
from modules.utils import logger
import json

def detect_waf(url, waf_signature_file="wafSignature.json"):
    """Detects if a WAF is present by analyzing response headers and content."""
    try:
        response = requests.get(url, timeout=5)
        with open(waf_signature_file, "r") as f:
            waf_signatures = json.load(f)

        for waf_name, signature in waf_signatures.items():
            if signature["headers"].lower() in str(response.headers).lower():
                logger.info(f"[+] Detected WAF: {waf_name}")
                return waf_name
        logger.info("[!] No WAF detected.")
        return None
    except Exception as e:
        logger.error(f"[-] WAF detection failed: {e}")
        return None
