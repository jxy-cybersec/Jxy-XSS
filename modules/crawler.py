import requests
from bs4 import BeautifulSoup

def crawl(url):
    """
    Crawls the target URL to extract endpoints.
    Args:
        url (str): Target URL to crawl.
    Returns:
        list: A list of dictionaries containing endpoint information.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        endpoints = []

        for form in forms:
            action = form.get("action", "")
            method = form.get("method", "get").lower()
            inputs = form.find_all("input")
            params = {}

            for inp in inputs:
                name = inp.get("name")
                if name:
                    params[name] = ""

            full_url = action if action.startswith("http") else url + action
            endpoints.append({"url": full_url, "params": params, "method": method})

        return endpoints
    except Exception as e:
        print(f"[-] Error during crawling: {e}")
        return []
