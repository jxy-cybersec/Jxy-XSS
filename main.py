import argparse
import subprocess
from modules.utils import setup_logger, save_results, default_headers
from modules.payloads import load_payloads_for_waf
from modules.target_analysis import analyze_target
from modules.injector import inject_payload
from modules.response_analysis import analyze_response
from modules.waf_detection import detect_waf
from modules.crawler import crawl

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
    author = "\n                # Author: JxyCyberSec\n"
    print(f"\033[94m{banner}\033[0m")
    print(f"\033[93m{author}\033[0m")


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

    if not args.url:
        logger.error("Please provide a target URL with -u or --url")
        return

    url = args.url
    headers = default_headers  # Use default headers from utils
    output_file = args.output

    logger.info(f"Starting scan for: {url}")

    waf_name = detect_waf(url, headers=headers)
    if waf_name:
        logger.info(f"Detected WAF: {waf_name}")
    else:
        logger.info("No WAF detected. Proceeding with default payloads.")

    payloads = load_payloads_for_waf(waf_name, base_path="payloads/")
    crawled_data = crawl(url, headers)  # Pass headers to the crawl function
    results = []

    for endpoint in crawled_data:
        logger.info(f"Testing endpoint: {endpoint['url']}")
        response_text = endpoint.get("response", "")
        analysis_result = analyze_target(response_text)
        results.append(analysis_result)

    if output_file:
        save_results(output_file, results)
        logger.info(f"Results saved to: {output_file}")

    logger.info("Scan complete.")


if __name__ == "__main__":
    main()
