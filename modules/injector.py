import copy
from modules.utils import replaceValue, requester
from modules.response_analysis import analyze_response

def inject_payload(url, params, payload, headers=None, method="GET"):
    """
    Injects a payload into the specified parameters and sends the request.
    """
    for param in params:
        modified_params = replaceValue(params, param, payload, copy.deepcopy)
        response = requester(url, params=modified_params, headers=headers, method=method)
        if analyze_response(response, payload):
            return response
    return None
