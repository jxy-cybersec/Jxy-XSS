import requests
import json
from modules.utils import logger
from termcolor import colored

def detect_waf(url, waf_signature_file="wafSignature.json"):
    """Detects WAF by analyzing headers & response."""
    try:
        response = requests.get(url, timeout=5)

        try:
            with open(waf_signature_file, "r") as f:
                waf_signatures = json.load(f)
        except FileNotFoundError:
            logger.error(colored("[-] WAF signature file missing! Skipping WAF detection.", "red"))
            return None

        for waf_name, signature in waf_signatures.items():
            if signature["headers"].lower() in str(response.headers).lower():
                logger.info(colored(f"🛡️ Detected WAF: {waf_name}", "yellow"))
                return waf_name
        
        logger.info(colored("[!] No WAF detected.", "cyan"))
        return None

    except Exception as e:
        logger.error(colored(f"[-] WAF detection failed: {e}", "red"))
        return None
