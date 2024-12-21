from modules.zetanize import zetanize
from modules.utils import handle_anchor, requester
from modules.colors import green, red, end


def crawl(url, headers=None):
    """
    Crawls the target for forms and injection points.

    Args:
        url (str): Target URL to crawl.
        headers (dict): Optional headers for HTTP requests.

    Returns:
        list: A list of endpoints with forms and input details.
    """
    if headers is None:
        headers = {}

    try:
        response = requester(url, headers=headers)
        if not response or not response.text:
            print(f"{red}[-] Unable to fetch content from {url}.{end}")
            return []

        forms = zetanize(response.text)
        endpoints = []

        for form_id, form in forms.items():
            action_url = handle_anchor(url, form["action"])
            endpoints.append({
                "url": action_url,
                "method": form["method"],
                "inputs": form["inputs"]
            })

        print(f"{green}[+] Found {len(endpoints)} endpoints during crawling.{end}")
        return endpoints
    except Exception as e:
        print(f"{red}[-] Error during crawling: {e}{end}")
        return []
