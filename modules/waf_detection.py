import requests

def detect_waf(url):
    try:
        response = requests.get(url, timeout=5)
        if "waf" in response.headers.get("Server", "").lower():
            return response.headers["Server"]
    except requests.RequestException as e:
        print(f"WAF detection error: {e}")
    return None
