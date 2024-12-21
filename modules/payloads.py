import os

def load_payloads_for_waf(waf_name=None, base_path="payloads/"):
    """
    Load WAF-specific or default payloads from the given directory.
    """
    payload_file = f"{base_path}/payloads_default.txt"
    if waf_name:
        specific_file = f"{base_path}/payloads_{waf_name.lower()}.txt"
        if os.path.exists(specific_file):
            payload_file = specific_file

    with open(payload_file, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]
