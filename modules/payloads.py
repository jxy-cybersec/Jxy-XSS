import os
import logging

logger = logging.getLogger("JXY-XSS")

def load_payloads(directory="payloads"):
    """
    Load payloads from files in the specified directory.

    Args:
        directory (str): Directory containing payload files.

    Returns:
        list: A list of all payloads from all files in the directory.
    """
    payloads = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    file_payloads = [line.strip() for line in file if line.strip()]
                    payloads.extend(file_payloads)
                    logger.info(f"Loaded {len(file_payloads)} payloads from {filename}.")
        return payloads
    except Exception as e:
        logger.error(f"[-] Failed to load payloads: {e}")
        raise RuntimeError(f"Failed to load payloads: {e}")
