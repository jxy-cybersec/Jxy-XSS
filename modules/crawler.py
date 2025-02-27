import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logger = logging.getLogger("JXY-XSS")

def crawl(url):
    """
    Crawl the given URL to discover additional endpoints and parameters.

    Args:
        url (str): The target URL to crawl.

    Returns:
        list: A list of discovered endpoints with their URLs and parameters.
    """
    try:
        logger.info(f"[*] Starting crawling for: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"[-] Failed to fetch URL {url}, Status Code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        endpoints = []

        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            endpoints.append({"url": full_url, "params": {}})

        for form in soup.find_all("form"):
            action = form.get("action")
            method = form.get("method", "get").lower()
            inputs = {input_tag.get("name", ""): input_tag.get("value", "") for input_tag in form.find_all("input")}
            form_url = urljoin(url, action) if action else url
            endpoints.append({"url": form_url, "params": inputs, "method": method})

        logger.info(f"[+] Found {len(endpoints)} endpoints during crawling.")
        return endpoints
    except Exception as e:
        logger.error(f"[-] Error during crawling: {e}")
        return []
