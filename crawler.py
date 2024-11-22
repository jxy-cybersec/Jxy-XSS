from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

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
                    "inputs": []
                }
                for input_tag in form.find_all("input"):
                    form_details["inputs"].append({
                        "name": input_tag.get("name"),
                        "type": input_tag.get("type", "text")
                    })
                forms.append(form_details)

            # Save the crawled page data
            crawled_data.append({
                "url": url,
                "forms": forms
            })
        except Exception as e:
            print(f"[!] Failed to crawl {url}: {e}")

        max_depth -= 1

    return crawled_data
