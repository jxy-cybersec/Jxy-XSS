import os

def load_payloads(file_path="payloads/payloads_default.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        raise RuntimeError(f"Failed to load payloads: {e}")
