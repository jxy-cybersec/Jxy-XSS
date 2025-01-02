import argparse
from modules.crawler import crawl
from modules.injector import inject_payload
from modules.payloads import load_payloads
from modules.waf_detection import detect_waf
from modules.utils import setup_logger

# Setup Logger
logger = setup_logger()

def banner():
    print(r"""
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
""")



def test_endpoint(url, payloads):
    """
    Function to test a specific endpoint with a list of payloads.
    """
    logger.info(f"Testing endpoint: {url}")
    for payload in payloads:
        try:
            response = inject_payload(url, {}, payload, headers={})
            if response:
                if payload in response.text:
                    logger.info(f"[+] Reflection detected: {payload}")
                    logger.info(f"[+] Vulnerable to payload: {payload}")
                else:
                    logger.debug(f"[-] No reflection for payload: {payload}")
        except Exception as e:
            logger.error(f"[-] Error during injection with payload {payload}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Jxy-XSS - XSS Vulnerability Scanner")
    parser.add_argument("-u", "--url", help="Target URL", required=True)
    args = parser.parse_args()

    url = args.url

    logger.info(f"Starting scan for: {url}")

    # WAF Detection
    logger.info("[*] Detecting WAF...")
    waf_name = detect_waf(url)
    if waf_name:
        logger.info(f"[+] Detected WAF: {waf_name}")
    else:
        logger.info("[!] No WAF detected. Proceeding with default payloads.")

    # Load payloads
    try:
        payloads = load_payloads()
        logger.info(f"Loaded {len(payloads)} payloads for testing.")
    except RuntimeError as e:
        logger.error(e)
        return

    # Direct endpoint testing if parameters are present in URL
    if "?" in url:
        logger.info(f"Testing provided endpoint directly: {url}")
        test_endpoint(url, payloads)
        return

    # Crawling if no parameters provided
    logger.info("Starting crawling...")
    try:
        crawled_endpoints = crawl(url)
        if not crawled_endpoints:
            logger.error("No endpoints found during crawling.")
            return
        logger.info(f"Found {len(crawled_endpoints)} endpoints during crawling.")
    except Exception as e:
        logger.error(f"Error during crawling: {e}")
        return

    # Testing crawled endpoints
    for endpoint in crawled_endpoints:
        test_endpoint(endpoint['url'], payloads)

if __name__ == "__main__":
    main()