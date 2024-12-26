import requests

def crawl(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return [{"url": url, "params": {}}]
    except Exception as e:
        print(f"[-] Error during crawling: {e}")
    return []
