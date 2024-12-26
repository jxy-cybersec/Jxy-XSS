import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("JXY-XSS")

def crawl(url, depth=1):
    """
    Crawls a URL to find endpoints with parameters.

    Args:
        url (str): The target URL to crawl.
        depth (int): The depth of crawling (default is 1).

    Returns:
        list: A list of discovered endpoints with their parameters.
    """
    logger.info(f"[*] Crawling: {url} (Depth: {depth})")
    discovered_endpoints = []

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            logger.error(f"[-] Failed to fetch {url}: HTTP {response.status_code}")
            return discovered_endpoints

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract links
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            if "?" in href:  # Check for query parameters
                full_url = href if href.startswith("http") else requests.compat.urljoin(url, href)
                discovered_endpoints.append({"url": full_url, "params": {}})
                logger.info(f"[+] Found endpoint: {full_url}")

        return discovered_endpoints

    except requests.RequestException as e:
        logger.error(f"[-] Error during crawling: {e}")
        return discovered_endpoints
