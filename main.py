import argparse

try:
    import subprocess  # Ensure subprocess is imported
    print(f"Subprocess module loaded from: {subprocess.__file__}")
except ImportError as e:
    print(f"Error importing subprocess: {e}")
    raise

from modules.utils import setup_logger, save_results
from modules.payloads import load_payloads_for_waf
from modules.target_analysis import crawl
from modules.injector import inject_payload
from modules.response_analysis import analyze_response
from modules.waf_detection import detect_waf

# Existing functions like print_banner(), get_arguments(), update_tool(), main(), etc.



def print_banner():
    """
    Prints the ASCII art banner and author information.
    """
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
    print(f"\033[94m{banner}\033[0m")  # Blue banner
    print(f"\033[93m{author}\033[0m")  # Yellow author info


def get_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="JXY-XSS - Automated XSS Vulnerability Scanner",
        epilog="Example usage: python main.py -u https://target.com -o results.json"
    )
    parser.add_argument("-u", "--url", help="Target URL to scan")
    parser.add_argument("-o", "--output", help="Path to save the scan results")
    parser.add_argument("-up", "--update", action="store_true", help="Update the tool to the latest version from GitHub")
    return parser.parse_args()


def update_tool():
    """
    Updates the tool by pulling the latest changes from GitHub.
    """
    logger = setup_logger()
    logger.info("Checking for updates...")
    try:
        # Run git pull using subprocess
        result = subprocess.run(
            ["git", "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "Already up to date." in result.stdout:
            logger.info("The tool is already up to date.")
        else:
            logger.info("Tool successfully updated to the latest version.")
            logger.info(result.stdout)
    except FileNotFoundError:
        logger.error("Git is not installed. Please install Git to use the update feature.")
    except Exception as e:
        logger.error(f"An error occurred while updating: {e}")


def main():
    # Print the banner
    print_banner()

    # Parse arguments
    args = get_arguments()
    logger = setup_logger()

    # Handle update functionality
    if args.update:
        update_tool()
        return

    # Ensure the URL argument is provided if not updating
    if not args.url:
        logger.error("Please provide a target URL with -u or --url")
        return

    url = args.url
    output_file = args.output
    logger.info(f"Starting scan for: {url}")

    # WAF Detection
    waf_name = detect_waf(url)
    if waf_name:
        logger.info(f"Detected WAF: {waf_name}")
    else:
        logger.info("No WAF detected. Proceeding with default payloads.")

    # Load payloads
    payloads = load_payloads_for_waf(waf_name, base_path="payloads/")

    # Crawl and test the target
    logger.info("Crawling target for injection points...")
    crawled_data = crawl(url)
    results = []

    for endpoint in crawled_data:
        logger.info(f"Testing endpoint: {endpoint['url']}")
        # Test URL parameters
        if endpoint['params']:
            logger.info(f"Testing query parameters: {list(endpoint['params'].keys())}")
            for payload in payloads:
                injected_results = inject_payload(endpoint['url'], endpoint['params'], payload)
                validated_results = analyze_response(injected_results)

                for param, payload in validated_results:
                    vulnerable_url = f"{endpoint['url'].split('?')[0]}?{param}={payload}"
                    logger.info(f"\033[92m[+] Verified Vulnerable URL: {vulnerable_url}\033[0m")
                    results.append({"url": endpoint['url'], "param": param, "payload": payload, "vulnerable_url": vulnerable_url})

        # Test forms
        for form in endpoint.get("forms", []):
            logger.info(f"\033[93mTesting form action: {form['action']}\033[0m")
            if form["params"]:
                logger.info(f"Testing form parameters: {list(form['params'].keys())}")
                for payload in payloads:
                    injected_results = inject_payload(form["action"], form["params"], payload, method=form["method"])
                    validated_results = analyze_response(injected_results)

                    for param, payload in validated_results:
                        vulnerable_url = f"{form['action']}?{param}={payload}"
                        logger.info(f"\033[92m[+] Verified Vulnerable URL: {vulnerable_url}\033[0m")
                        results.append({"url": form['action'], "param": param, "payload": payload, "vulnerable_url": vulnerable_url})

    # Save results to file if specified
    if output_file:
        save_results(output_file, results)
        logger.info(f"Results saved to: {output_file}")

    logger.info("Scan complete. Check results for details.")


if __name__ == "__main__":
    main()
