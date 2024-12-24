import json
import re
from modules.utils import requester

def detect_waf(url, headers, payload="<script>alert(1)</script>"):
    """
    Detects if a WAF is present on the target URL.
    Returns the name of the WAF if detected, otherwise None.
    """
    try:
        with open("db/wafSignatures.json") as f:
            waf_signatures = json.load(f)

        print("[*] Checking for WAF...")
        response = requester(url, params={"xss": payload}, headers=headers)
        
        for waf_name, signatures in waf_signatures.items():
            if re.search(signatures["page"], response.text, re.I):
                print(f"[+] WAF detected: {waf_name}")
                return waf_name
        
        print("[-] No WAF detected.")
    except Exception as e:
        print(f"[-] Error during WAF detection: {e}")
    return None
