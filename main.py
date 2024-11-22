import argparse
from modules.utils import setup_logger, save_results
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
    parser.add_argument("-o", "--output", required=False, help="Path to save the scan results")
    return parser.parse_args()

def main():
    # Setup logger
    logger = setup_logger()

    # Parse arguments
    args = get_arguments()
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
                for param, payload, response_text in injected_results:
                    if payload in response_text:
                        vulnerable_url = f"{endpoint['url']}?{param}={payload}"
                        logger.info(f"[+] Vulnerable URL: {vulnerable_url}")
                        results.append({"url": endpoint['url'], "param": param, "payload": payload, "vulnerable_url": vulnerable_url})

        # Test forms
        for form in endpoint.get("forms", []):
            logger.info(f"Testing form action: {form['action']}")
            if form["params"]:
                logger.info(f"Testing form parameters: {list(form['params'].keys())}")
                for payload in payloads:
                    injected_results = inject_payload(form["action"], form["params"], payload, method=form["method"])
                    for param, payload, response_text in injected_results:
                        if payload in response_text:
                            vulnerable_url = f"{form['action']}?{param}={payload}"
                            logger.info(f"[+] Vulnerable URL: {vulnerable_url}")
                            results.append({"url": form['action'], "param": param, "payload": payload, "vulnerable_url": vulnerable_url})

    # Save results to file if specified
    if output_file:
        save_results(output_file, results)
        logger.info(f"Results saved to: {output_file}")

    logger.info("Scan complete. Check results for details.")

if __name__ == "__main__":
    main()
