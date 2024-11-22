from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse, parse_qs

def crawl(base_url, max_depth=2):
    """
    Crawls the target website to discover pages and forms.
    """
    visited = set()
    to_visit = [base_url]
    crawled_data = []

    while to_visit and max_depth > 0:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")

            # Extract all links
            for link in soup.find_all("a", href=True):
                full_url = urljoin(base_url, link["href"])
                if full_url not in visited and base_url in full_url:
                    to_visit.append(full_url)

            # Extract forms on the page
            forms = []
            for form in soup.find_all("form"):
                form_details = {
                    "action": urljoin(base_url, form.get("action", "")),
                    "method": form.get("method", "GET").upper(),
                    "params": {}
                }
                for input_tag in form.find_all("input"):
                    input_name = input_tag.get("name")
                    if input_name:
                        form_details["params"][input_name] = ""  # Initialize with empty value
                forms.append(form_details)

            # Save the crawled page data
            crawled_data.append({
                "url": url,
                "forms": forms,
                "params": parse_qs(urlparse(url).query)  # Extract query params from URL
            })
        except requests.RequestException as e:
            print(f"[!] Failed to crawl {url}: {e}")

        max_depth -= 1

    return crawled_data
