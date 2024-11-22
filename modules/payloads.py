import os

def load_payloads(file_path):
    """
    Loads payloads from a file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file]
    except Exception as e:
        print(f"[!] Error loading payloads from {file_path}: {e}")
        return []

def load_payloads_for_waf(waf_name=None, base_path="payloads/"):
    """
    Load payloads based on the detected WAF or default payloads if no WAF is found.
    """
    file_map = {
        "CloudFront": os.path.join(base_path, "payloads_cloudfront.txt"),
        "Akamai": os.path.join(base_path, "payloads_akamai.txt"),
        "CloudFlare": os.path.join(base_path, "payloads_cloudflare.txt"),
        "Imperva": os.path.join(base_path, "payloads_imperva.txt"),
        "Incapsula": os.path.join(base_path, "payloads_incapsula.txt"),
        "Wordfence": os.path.join(base_path, "payloads_wordfence.txt"),
    }
    file_path = file_map.get(waf_name, os.path.join(base_path, "payloads_default.txt"))
    print(f"[*] Using payloads from: {file_path}")
    return load_payloads(file_path)
