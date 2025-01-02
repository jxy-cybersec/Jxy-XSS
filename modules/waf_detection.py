import requests

def detect_waf(url):
    """
    Detects the presence of a Web Application Firewall (WAF).

    Args:
        url (str): Target URL.

    Returns:
        str: Name of the detected WAF, or None if no WAF is detected.
    """
    try:
        response = requests.get(url, timeout=5)
        if response.status_code in [403, 406]:
            headers = response.headers
            if "cloudflare" in headers.get("Server", "").lower():
                return "Cloudflare"
            if "akamai" in headers.get("Server", "").lower():
                return "Akamai"
            if "aws-waf" in headers.get("x-amzn-requestid", "").lower():
                return "AWS WAF"
            if "imperva" in headers.get("x-cdn", "").lower():
                return "Imperva SecureSphere"
            if "f5" in headers.get("Server", "").lower():
                return "F5 BIG-IP ASM"
            if "mod_security" in headers.get("Server", "").lower():
                return "ModSecurity"
        return None
    except requests.RequestException as e:
        print(f"[-] WAF detection error: {e}")
        return None
