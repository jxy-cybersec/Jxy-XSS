from modules.zetanize import zetanize
from modules.utils import handle_anchor, requester

def crawl(url, headers):
    """
    Crawls the target for forms and injection points.
    """
    response = requester(url, headers=headers)
    forms = zetanize(response.text)
    endpoints = []

    for form_id, form in forms.items():
        action_url = handle_anchor(url, form["action"])
        endpoints.append({
            "url": action_url,
            "method": form["method"],
            "inputs": form["inputs"]
        })
    return endpoints
