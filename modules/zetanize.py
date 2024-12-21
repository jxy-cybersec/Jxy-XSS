import re

def zetanize(response):
    """
    Extracts forms and input fields from the HTML response.
    """
    forms = {}
    form_matches = re.findall(r'(?i)(?s)<form.*?>.*?</form>', response)
    for idx, form in enumerate(form_matches):
        action = re.search(r'action=["\']?(.*?)["\']', form, re.I)
        method = re.search(r'method=["\']?(.*?)["\']', form, re.I)
        inputs = re.findall(r'<input.*?>', form, re.I)

        forms[idx] = {
            "action": action.group(1) if action else '',
            "method": method.group(1).lower() if method else 'get',
            "inputs": {}
        }

        for inp in inputs:
            name = re.search(r'name=["\']?(.*?)["\']', inp, re.I)
            inp_type = re.search(r'type=["\']?(.*?)["\']', inp, re.I)
            value = re.search(r'value=["\']?(.*?)["\']', inp, re.I)
            forms[idx]["inputs"][name.group(1) if name else ''] = {
                "type": inp_type.group(1).lower() if inp_type else 'text',
                "value": value.group(1) if value else ''
            }

    return forms
