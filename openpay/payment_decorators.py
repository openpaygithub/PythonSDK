import requests
import lxml.etree
from .payload import buildxml_string
from .utils import handle_response

headers = {'Content-Type': "application/xml", 'Cache-Control': "no-cache"}


def prepare_response(input_func):
    """
    :param input_func: Input function on which this wrapper will work.
    :return: Response Openpay response for input function.
    """
    def wrapper(self, **kwargs):
        func_resp = input_func(self, **kwargs)
        if "http_method" in func_resp and func_resp["http_method"] == "POST":
            payload = buildxml_string(func_resp["url"], func_resp["attr_dict"])
            response = requests.request(func_resp["http_method"], func_resp["url"], data=payload, headers=headers)
            xml_response = response.text
            root = lxml.etree.fromstring(xml_response)
            resp = handle_response(root=root)

            if resp.get('PlanID', None) is not None:
                print(type(resp['PlanID']))
                self.plan_id = resp.get('PlanID')
            return resp
        elif "http_method" in func_resp and func_resp["http_method"] == "GET":
            header = func_resp["headers"] if func_resp.get("headers", None) is not None else ""
            response = requests.request("GET", func_resp["url"], headers=header, params=func_resp["params"])
            return response.url
        else:
            return func_resp
    return wrapper
