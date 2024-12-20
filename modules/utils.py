import requests
import json
import random
import re

def requester(url, params=None, headers=None, method="GET"):
    """
    Sends an HTTP request to the target URL.
    """
    if method.upper() == "GET":
        response = requests.get(url, params=params, headers=headers)
    else:
        response = requests.post(url, data=params, headers=headers)
    return response
