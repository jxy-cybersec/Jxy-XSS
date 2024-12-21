import argparse
import time
from modules.utils import setup_logger, save_results
from modules.payloads import load_payloads_for_waf
from modules.crawler import crawl
from modules.injector import inject_payload
from modules.waf_detection import detect_waf

logger = setup_logger()

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
    print(f"\033[94m{banner}\033[0m")


def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="XSS Scanner Tool")
    parser.add_argument("-u", "--url", required=True, help="Target URL to scan")
    parser.add_argument("-o", "--output", help="File to save results (JSON format)")
    args = parser.parse_args()

    # Banner
    print_banner()

    url = args.url
    output_file = args.output

    logger.info(f"Starting scan for: {url}")

    # WAF Detection
    waf_name = detect_waf(url, headers={})
    if waf_name:
        logger.info(f"WAF detected: {waf_name}")
    else:
        logger.info("No WAF detected.")

    # Load Payloads
    payloads = load_payloads_for_waf()
    logger.info(f"Loaded {len(payloads)} payloads for testing.")

    # Crawling the target
    crawled_data = crawl(url, headers={})
    logger.info(f"Found {len(crawled_data)} endpoints during crawling.")

    # Initialize results
    vulnerabilities = []

    # Testing each endpoint
    for endpoint in crawled_data:
        endpoint_url = endpoint.get('url', None)
        params = endpoint.get('params', {})

        if not endpoint_url:
            logger.warning(f"Skipping an endpoint without a valid URL: {endpoint}")
            continue

        logger.info(f"Testing endpoint: {endpoint_url}")
        for payload in payloads:
            try:
                response = inject_payload(endpoint_url, params, payload, headers={})
                if response:
                    logger.info(f"[+] Reflection detected with payload: {payload}")
                    vulnerabilities.append({"url": endpoint_url, "payload": payload})

                # Enforce rate limit of 10 payloads/sec
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"[-] Error during injection with payload {payload}: {e}")

    # Save results
    if vulnerabilities:
        logger.info(f"[+] Found {len(vulnerabilities)} vulnerabilities.")
        if output_file:
            save_results(output_file, vulnerabilities)
            logger.info(f"Results saved to: {output_file}")
    else:
        logger.info("[-] No vulnerabilities found.")

    logger.info("Scan complete.")


if __name__ == "__main__":
    main()
