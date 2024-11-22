import argparse
from modules.utils import setup_logger
from modules.payloads import load_payloads_for_waf
from modules.target_analysis import crawl
from modules.injector import inject_payload
from modules.response_analysis import analyze_response
from modules.waf_detection import detect_waf

def get_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="JXY-XSS - Automated XSS Vulnerability Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target URL to scan")
    return parser.parse_args()

def main():
    # Setup logger
    logger = setup_logger()

    # Parse arguments
    args = get_arguments()
    url = args.url
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

    for endpoint in crawled_data:
        logger.info(f"Testing endpoint: {endpoint['url']}")
        # Test URL parameters
        if endpoint['params']:
            logger.info(f"Testing query parameters: {list(endpoint['params'].keys())}")
            for payload in payloads:
                results = inject_payload(endpoint['url'], endpoint['params'], payload)
                analyze_response(results)

        # Test forms
        for form in endpoint.get("forms", []):
            logger.info(f"Testing form action: {form['action']}")
            if form["params"]:
                logger.info(f"Testing form parameters: {list(form['params'].keys())}")
                for payload in payloads:
                    results = inject_payload(form["action"], form["params"], payload, method=form["method"])
                    analyze_response(results)

    logger.info("Scan complete. Check results for details.")

if __name__ == "__main__":
    main()
