import argparse
from modules.crawler import crawl
from modules.injector import inject_payload
from modules.payloads import load_payloads
from modules.utils import setup_logger, update_tool
from modules.analysis import validate_response
from modules.waf_detection import detect_waf
from termcolor import colored  # For colored output

# Setup Logger
logger = setup_logger()


def banner():
    print(colored(r"""
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
""", "cyan"))


def process_urls(file_path):
    """Read URLs from a file and test each for XSS."""
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    for url in urls:
        logger.info(colored(f"Processing URL: {url}", "cyan"))
        scan_url(url)


def scan_url(url):
    """Scan a single URL for XSS vulnerabilities."""
    logger.info(colored(f"Starting scan for: {url}", "cyan"))

    # Detect WAF
    waf_name = detect_waf(url)
    if waf_name:
        logger.info(colored(f"[+] Detected WAF: {waf_name}", "yellow"))
    else:
        logger.info(colored("[!] No WAF detected.", "yellow"))

    # Load payloads
    payloads = load_payloads()
    logger.info(colored(f"Loaded {len(payloads)} payloads for testing.", "cyan"))

    # Test provided endpoint
    logger.info(colored(f"Testing endpoint: {url}", "yellow"))
    for payload in payloads:
        try:
            response = inject_payload(url, {}, payload)
            if response:
                if validate_response(response, payload):
                    logger.info(colored(f"[+] Vulnerable to XSS with payload: {payload}", "green"))
                else:
                    logger.info(colored(f"[-] Payload not executed: {payload}", "red"))
            else:
                logger.info(colored(f"[-] No response received for payload: {payload}", "red"))
        except Exception as e:
            logger.error(colored(f"[-] Error during injection with payload {payload}: {e}", "red"))


def main():
    parser = argparse.ArgumentParser(description="JXY-XSS - XSS Vulnerability Scanner")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-uf", "--url-file", help="File containing list of URLs")
    parser.add_argument("--update", action="store_true", help="Update the tool")

    args = parser.parse_args()

    if args.update:
        update_tool()
        return

    banner()

    if args.url_file:
        process_urls(args.url_file)
    elif args.url:
        scan_url(args.url)
    else:
        logger.error(colored("Please provide a target URL or a file containing URLs.", "red"))


if __name__ == "__main__":
    main()
