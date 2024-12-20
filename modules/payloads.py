def load_payloads_for_waf(waf_name=None, base_path="payloads/"):
    """
    Load WAF-specific or default payloads from the given directory.
    """
    payload_file = f"{base_path}/payloads_default.txt"
    if waf_name:
        specific_file = f"{base_path}/payloads_{waf_name.lower()}.txt"
        try:
            with open(specific_file, "r") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            pass  # Fall back to default if WAF-specific file is not found

    with open(payload_file, "r") as file:
        return [line.strip() for line in file if line.strip()]
