import argparse
import subprocess
from modules.utils import setup_logger, save_results
from modules.payloads import load_payloads_for_waf
from modules.target_analysis import analyze_target
from modules.injector import inject_payload
from modules.response_analysis import analyze_response
from modules.waf_detection import detect_waf
from modules.crawler import crawl
from modules.payloads import generate_payloads


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


def update_tool(logger):
    logger.info("Checking for updates...")
    try:
        result = subprocess.run(
            ["git", "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "Already up to date." in result.stdout:
            logger.info("The tool is already up to date.")
        else:
            logger.info("Tool successfully updated.")
    except FileNotFoundError:
        logger.error("Git is not installed. Please install Git to use the update feature.")
    except Exception as e:
        logger.error(f"An error occurred while updating: {e}")


def test_payloads(endpoint, payloads, logger):
    results = []
    params = endpoint.get('params', {})  # Ensure params is always a dictionary

    if not isinstance(params, dict):
        logger.error("[-] Invalid parameters format. Expected dict.")
        return []

    for payload in payloads:
        logger.info(f"[*] Testing payload: {payload}")
        injected_results = inject_payload(endpoint['url'], params, payload)
        results.extend(injected_results)

    return results


def main():
    print_banner()
    logger = setup_logger()
    args = get_arguments()

    if args.update:
        update_tool(logger)
        return

    if not args.url:
        logger.error("Please provide a target URL with -u or --url")
        return

    url = args.url
    output_file = args.output
    logger.info(f"Starting scan for: {url}")

    waf_name = detect_waf(url)
    if waf_name:
        logger.info(f"Detected WAF: {waf_name}")
    else:
        logger.info("No WAF detected. Proceeding with default payloads.")

    payloads = load_payloads_for_waf(waf_name, base_path="payloads/")
    crawled_data = crawl(url)
    logger.info(f"[+] Found {len(crawled_data)} endpoints during crawling.")
    for endpoint in crawled_data:
        logger.debug(f"Endpoint structure: {endpoint}")

    results = []
    for endpoint in crawled_data:
        logger.info(f"Testing endpoint: {endpoint['url']}")
        
        # Ensure 'response' is passed correctly
        response_text = endpoint.get('response', '')  # Get raw response text
        html_contexts = analyze_target(response_text)  # Pass raw text to analyze_target
        
        for context, details in html_contexts.get('html_contexts', {}).items():
            payloads = generate_payloads(context, details)
            results.extend(test_payloads(endpoint, payloads, logger))

    if output_file:
        save_results(output_file, results)
        logger.info(f"Results saved to: {output_file}")

    logger.info("Scan complete.")


if __name__ == "__main__":
    main()
