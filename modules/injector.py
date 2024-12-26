import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger("JXY-XSS")

def crawl(url):
    """
    Crawls the given URL to find links and parameters.

    Args:
        url (str): The target URL.

    Returns:
        list: A list of crawled endpoints with parameters.
    """
    crawled_endpoints = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link['href']
                if href.startswith("http"):
                    crawled_endpoints.append({"url": href, "params": {}})
                elif href.startswith("/"):
                    crawled_endpoints.append({"url": url.rstrip("/") + href, "params": {}})
        return crawled_endpoints
    except Exception as e:
        logger.error(f"[-] Error during crawling: {e}")
    return []
