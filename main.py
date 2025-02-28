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

def scan_file(file_path):
    """Scan multiple URLs from a file."""
    try:
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file if line.strip()]

        if not urls:
            logger.error(colored("⚠️ No URLs found in file!", "red"))
            return
        
        logger.info(colored(f"📄 Scanning {len(urls)} URLs from file: {file_path}", "cyan"))
        for url in urls:
            scan_url(url)

    except FileNotFoundError:
        logger.error(colored(f"❌ File not found: {file_path}", "red"))
    except Exception as e:
        logger.error(colored(f"❌ Error reading file: {e}", "red"))

def main():
    parser = argparse.ArgumentParser(description="JXY-XSS - XSS Scanner")
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-uf", "--url-file", help="File containing list of URLs")
    parser.add_argument("--update", action="store_true", help="Update tool")

    args = parser.parse_args()

    if args.update:
        update_tool()
        return

    if args.url_file:
        scan_file(args.url_file)
    elif args.url:
        scan_url(args.url)
    else:
        logger.error(colored("⚠️ Please provide a URL or file!", "red"))

if __name__ == "__main__":
    banner()
    main()
