import logging
import json

def setup_logger():
    """
    Sets up the logger for JXY-XSS.
    """
    logging.basicConfig(
        format='[%(asctime)s] [JXY-XSS] [%(levelname)s]: %(message)s',
        level=logging.INFO
    )
    return logging.getLogger("JXY-XSS")

def save_results(file_path, results):
    """
    Saves the scan results to a file in JSON format.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)
        print(f"[+] Results saved to {file_path}")
    except IOError as e:
        print(f"[!] Failed to save results: {e}")
