import argparse
from modules.crawler import crawl
from modules.injector import inject_payload
from modules.payloads import load_payloads
from modules.utils import setup_logger, update_tool
from modules.analysis import validate_response
from modules.waf_detection import detect_waf
from termcolor import colored

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

def scan_url(url):
    """Scan URL for XSS vulnerabilities."""
    logger.info(colored(f"🔍 Scanning: {url}", "cyan"))

    waf_name = detect_waf(url)
    
    # Load payloads
    payloads = load_payloads()
    logger.info(colored(f"📦 Loaded {len(payloads)} payloads.", "cyan"))

    # Test endpoint
    logger.info(colored(f"⚡ Testing endpoint: {url}", "yellow"))
    for payload in payloads:
        inject_payload(url, {}, payload)

def main():
    parser = argparse.ArgumentParser(description="JXY-XSS - XSS Scanner")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("--update", action="store_true", help="Update tool")

    args = parser.parse_args()

    if args.update:
        update_tool()
        return

    if args.url:
        scan_url(args.url)
    else:
        logger.error(colored("⚠️ Please provide a URL!", "red"))

if __name__ == "__main__":
    banner()
    main()
