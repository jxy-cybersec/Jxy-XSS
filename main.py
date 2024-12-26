import argparse
import subprocess
from modules.utils import setup_logger, save_results, update_tool
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
    
                # Author: JxyCyberSec
    """
    print(banner)


def get_arguments():
    parser = argparse.ArgumentParser(
        description="JXY-XSS - Automated XSS Vulnerability Scanner",
        epilog="Example usage: python main.py -u https://target.com -o results.json"
    )
    parser.add_argument("-u", "--url", help="Target URL to scan")
    parser.add_argument("-o", "--output", help="Path to save the scan results")
    parser.add_argument("-up", "--update", action="store_true", help="Update the tool to the latest version from GitHub")
    return parser.parse_args()


def main():
    print_banner()
    args = get_arguments()
    logger = setup_logger()

    if args.update:
        update_tool(logger)
        return

    if not args.url:
        logger.error("Please provide a target URL with -u or --url")
        return

    url = args.url
    headers = {}
    logger.info(f"Starting scan for: {url}")

    # Skip crawling if a specific URL is provided
    endpoints = [{"url": url, "params": {}}]
    payloads = load_payloads("default")
    logger.info(f"Loaded {len(payloads)} payloads for testing.")

    if not endpoints:
        logger.error("No endpoints found during crawling.")
        return

    for endpoint in endpoints:
        logger.info(f"Testing endpoint: {endpoint['url']}")
        for payload in payloads:
            inject_payload(endpoint['url'], endpoint.get('params', {}), payload, headers)


if __name__ == "__main__":
    main()
