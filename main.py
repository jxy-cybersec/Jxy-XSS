import argparse
import subprocess
from modules.utils import setup_logger, save_results
from modules.payloads import load_payloads_for_waf, generate_payloads
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


def update_tool():
    logger = setup_logger()
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


def test_payloads(endpoint, payloads):
    results = []
    for payload in payloads:
        response = inject_payload(endpoint['url'], endpoint['params'], payload)
        if analyze_response(response, payload):
            results.append({
                "url": endpoint['url'],
                "payload": payload
            })
    return results


def main():
    print_banner()
    args = get_arguments()
    logger = setup_logger()

    if args.update:
        update_tool()
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
    results = []

    for endpoint in crawled_data:
        logger.info(f"Testing endpoint: {endpoint['url']}")
        html_contexts = htmlParser(endpoint['response'])
        for context, details in html_contexts.items():
            payloads = generate_payloads(context, details)
            results.extend(test_payloads(endpoint, payloads))

    if args.output:
        save_results(args.output, results)
        logger.info(f"Results saved to: {args.output}")

    logger.info("Scan complete.")


if __name__ == "__main__":
    main()
