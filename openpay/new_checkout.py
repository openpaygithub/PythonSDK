from .utils import check_date_format, check_postal_code
from collections import OrderedDict
from .payment_decorators import prepare_response

no_merchant_found = {"status": False, "message": "No merchant is associated with this client..", "value": None}


class Merchant(object):
    '''
    Create a merchant using JamAuthToken and Authtoken
    '''
    def __init__(self, jam_token, auth_token=None):
        self.JamAuthToken = jam_token
        self.AuthToken =  auth_token or self.JamAuthToken.split('|')[1]
        self.JamCallbackURL, self.JamCancelURL, self.JamFailURL = None, None, None

    def set_callback_url(self, callback_url=None, cancel_url=None, failure_url=None):
        """
        :param callback_url: A URL where we will redirected after successful payment through Openpay.
        :param cancel_url: A URL where we will redirected after cancel payment through Openpay.
        :param failure_url: A URL where we will redirected after unsuccessful payment through Openpay.
        :return: client object
        """
        self.JamCallbackURL = callback_url
        self.JamCancelURL = cancel_url
        self.JamFailURL = failure_url


class Client(object):
    '''
    Create a client under a merchant
    '''

    def __init__(self, merchant, **kwargs):
        self.merchant = merchant
        for key, value in kwargs.items():
            if key in ['dob', 'delivery_date']:
                val = check_date_format(kwargs.get(key, None))
                setattr(self, key, val)
            elif key == 'postcode':
                self.postcode = check_postal_code(value)
            else:
                setattr(self, key, kwargs.get(key, None))
        self.plan_id, self.price, self.plan_creation_type = None, None, None

    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['dob', 'delivery_date']:
                val = check_date_format(kwargs.get(key, None))
                setattr(self, key, val)
            elif key == 'postcode':
                self.postcode = check_postal_code(value)
            else:
                setattr(self, key, kwargs.get(key, None))

    def find_merchant(self):
            if getattr(self, "merchant", None) is None:
                return no_merchant_found
            return {"status": True}

    @prepare_response
    def min_max_purchase_price(self):
        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token)])
        url = "https://retailer.myopenpay.com.au/ServiceTraining/JAMServiceImpl.svc/MinMaxPurchasePrice"
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    def is_valid_price(self, price):
        resp = self.min_max_purchase_price()
        if resp["status"] == 0:
            max_price = resp["MaxPrice"]
            min_price = resp["MinPrice"]
            if float(resp["MinPrice"]) <= price <= float(resp["MaxPrice"]):
                return {"status": True, "error": ""}
            return {"status": False, "error": "You purchase price is not under min-max range ({} to {})".format(
                min_price, max_price)}
        return resp

    @prepare_response
    def new_online_order(self, **kwargs):
        check_merchant = self.find_merchant()
        if not check_merchant["status"]:
            return no_merchant_found
        purchase_price, plan_creation_type = kwargs.get("purchase_price", None), kwargs.get("plan_creation_type", None)
        validate_price_resp = self.is_valid_price(price=purchase_price)
        if int(validate_price_resp["status"]) > 0:
            return validate_price_resp

        self.price = purchase_price
        self.plan_creation_type = plan_creation_type
        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token),
                                 ("purchase_price", purchase_price), ("plan_creation_type", plan_creation_type)])
        url = "https://retailer.myopenpay.com.au/ServiceTraining/JAMServiceImpl.svc/NewOnlineOrder"
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    @prepare_response
    def create_online_plan(self):
        check_merchant = self.find_merchant()
        if not check_merchant["status"]:
            return no_merchant_found

        querystring = {
            "JamCallbackURL": self.merchant.JamCallbackURL,
            "JamCancelURL": self.merchant.JamCancelURL,
            "JamFailURL": self.merchant.JamFailURL,
            "JamAuthToken": self.merchant.JamAuthToken,
            "JamPlanID": self.plan_id,
            "JamRetailerOrderNo": str(self.order_id),
            "JamPrice": str(self.price),
            "JamFirstName": self.first_name,
            "JamFamilyName": self.family_name,
            "JamEmail": self.email,
            "JamAddress1": self.address_1,
            "JamSuburb": self.suburb,
            "JamState": self.state,
            "JamPostcode": str(self.postcode)
        }
        headers = {'Cache-Control': "no-cache"}
        url = "https://retailer.myopenpay.com.au/WebSalesTraining/"
        return {"url": url, "http_method": "GET", "params": querystring, "headers": headers}

    @prepare_response
    def check_payment_capture(self, plan_id):
        check_merchant = self.find_merchant()
        if not check_merchant["status"]:
            return no_merchant_found

        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token),
                                 ("plan_iD", plan_id)])
        url = "https://retailer.myopenpay.com.au/ServiceTraining/JAMServiceImpl.svc/OnlineOrderCapturePayment"
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    @prepare_response
    def check_order_status(self, plan_id):
        check_merchant = self.find_merchant()
        if not check_merchant["status"]:
            return no_merchant_found

        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token),
                                 ("plan_iD", plan_id)])
        url = "https://retailer.myopenpay.com.au/ServiceTraining/JAMServiceImpl.svc/OnlineOrderStatus"
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    @prepare_response
    def refund_status(self, plan_id, **kwargs):
        check_merchant = self.find_merchant()
        if not check_merchant["status"]:
            return no_merchant_found

        new_purchase_price = 0.00 if kwargs.get("full_refund", False) else kwargs["new_purchase_price"]
        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token), ("plan_iD", plan_id),
                                 ("new_purchase_price", new_purchase_price), ("full_refund", kwargs.get("full_refund",
                                                                                                        False))])
        url = "https://retailer.myopenpay.com.au/ServiceTraining/JAMServiceImpl.svc/OnlineOrderReduction"
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    @prepare_response
    def order_dispatch_plan(self, plan_id, **kwargs):
        check_merchant = self.find_merchant()
        if not check_merchant["status"]:
            return no_merchant_found
        jam_auth_token = self.merchant.JamAuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("plan_id", plan_id)])
        url = "https://retailer.myopenpay.com.au/ServiceTraining/JAMServiceImpl.svc/OnlineOrderDispatchPlan"
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}
