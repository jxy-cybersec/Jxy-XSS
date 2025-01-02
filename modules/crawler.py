import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger("JXY-XSS")

def crawl(url):
    """
    Crawl the target URL to find potential injection points.
    """
    endpoints = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                endpoints.append({"url": link["href"], "params": {}})
            logger.info(f"[+] Found {len(endpoints)} endpoints during crawling.")
        else:
            logger.warning(f"[!] Received non-200 status code: {response.status_code}")
    except Exception as e:
        logger.error(f"[-] Error during crawling: {e}")
    return endpoints
