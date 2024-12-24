import os

def load_payloads(payload_type):
    """
    Load payloads of the given type from the appropriate file.
    """
    payload_file = f"payloads/payloads_{payload_type}.txt"
    if not os.path.exists(payload_file):
        raise FileNotFoundError(f"Payload file '{payload_file}' not found.")

    try:
        with open(payload_file, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except UnicodeDecodeError as e:
        print(f"[-] Error reading {payload_file}: {e}")
        return []
