import argparse
import time
from modules.utils import setup_logger
from modules.payloads import load_payloads
from modules.crawler import crawl
from modules.injector import inject_payload

def print_banner():
    banner = r"""
     ▄█ ▀████    ▐████▀ ▄██   ▄   ▀████    ▐████▀    ▄████████    ▄████████
    ███   ███▌   ████▀  ███   ██▄   ███▌   ████▀    ███    ███   ███    ███
    ███    ███  ▐███    ███▄▄▄███    ███  ▐███      ███    █▀    ███    █▀
    ███    ▀███▄███▀    ▀▀▀▀▀▀███    ▀███▄███▀      ███          ███
    ███    ████▀██▄     ▄██   ███    ████▀██▄     ▀███████████ ▀███████████
    ███   ▐███  ▀███    ███   ███   ▐███  ▀███             ███          ███
    ███  ▄███     ███▄  ███   ███  ▄███     ███▄     ▄█    ███    ▄█    ███
█▄ ▄███ ████       ███▄  ▀█████▀  ████       ███▄  ▄████████▀   ▄████████▀
▀▀▀▀▀▀
    """
    print(banner)
    print("\n                # Author: JxyCyberSec\n")

def get_arguments():
    parser = argparse.ArgumentParser(
        description="JXY-XSS - Advanced XSS Scanner with Payload Mutation",
        epilog="Example: python main.py -u https://target.com -o results.json"
    )
    parser.add_argument("-u", "--url", help="Target URL to scan", required=True)
    parser.add_argument("-o", "--output", help="Path to save the scan results", default="results.json")
    parser.add_argument("-t", "--type", help="Type of payloads to use (default, js)", default="default")
    return parser.parse_args()

def main():
    print_banner()
    args = get_arguments()
    logger = setup_logger()

    url = args.url
    output_file = args.output
    payload_type = args.type

    logger.info(f"Starting scan for: {url}")

    # Load payloads
    payloads = load_payloads(payload_type)
    if not payloads:
        logger.error("No payloads loaded. Please check your payload files.")
        return
    logger.info(f"Loaded {len(payloads)} payloads for testing.")

    # Crawl the target
    crawled_data = crawl(url)
    if not crawled_data:
        logger.error("No endpoints found during crawling.")
        return
    logger.info(f"Found {len(crawled_data)} endpoints during crawling.")

    # Perform injections
    for endpoint in crawled_data:
        logger.info(f"Testing endpoint: {endpoint['url']}")
        for payload in payloads:
            if inject_payload(endpoint['url'], endpoint['params'], payload, headers={}):
                logger.info(f"[+] Found vulnerable payload: {payload}")

    logger.info("Scan complete.")

if __name__ == "__main__":
    main()
