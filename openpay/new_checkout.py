from .utils import check_date_format, check_postal_code
from collections import OrderedDict
from .payment_decorators import prepare_response

no_merchant_found = {"status": False, "message": "No merchant is associated with this client..", "value": None}
no_order_id = {"status": False, "message": "No order number is associated to create online plan"}


class Merchant(object):
    """
    Create a merchant using JamAuthToken and(or) AuthToken
    """

    def __init__(self, jam_token, country_code, auth_token=None, openpay_url_mode="Live"):
        self.JamAuthToken = jam_token
        self.AuthToken = auth_token or self.JamAuthToken.split('|')[1]
        self.OpenURLMode = openpay_url_mode
        self.JamCallbackURL, self.JamCancelURL, self.JamFailURL = None, None, None
        if isinstance(country_code, str) and country_code.lower() in ['uk', 'au']:
            self.country_code = country_code.lower()
        else:
            raise ValueError("Country code must be in 'uk' or 'au' in Merchant object ")
        if self.country_code == 'au':
            self.url = "https://retailer.myopenpay.com.au/Service{}/JAMServiceImpl.svc/"
            self.handover_url = "https://retailer.myopenpay.com.au/WebSales{}/"

        elif self.country_code == 'uk':
            self.url = "https://integration.{}myopenpay.co.uk/JamServiceImpl.svc/"
            self.handover = "https://websales.{}.myopenpay.co.uk/"

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

    @prepare_response
    def online_order_fraud_alert(self, plan_id):
        jam_auth_token = self.JamAuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("plan_id", plan_id)])
        url = self.url + "OnlineOrderFraudAlert".format(
            self.OpenURLMode)
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}


class Client(object):
    """
    Create a client under a merchant
    """

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
        self.url = self.merchant.url
        self.handover_url = self.merchant.handover_url

    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['dob', 'delivery_date']:
                val = check_date_format(kwargs.get(key, None))
                setattr(self, key, val)
            elif key == 'postcode':
                self.postcode = check_postal_code(value)
            else:
                setattr(self, key, kwargs.get(key, None))

    @prepare_response
    def new_online_order(self, **kwargs):
        purchase_price, plan_creation_type = kwargs.get("purchase_price", None), kwargs.get("plan_creation_type", None)
        validate_price_resp = self.is_valid_price(price=purchase_price)
        if not validate_price_resp["status"]:
            return validate_price_resp

        self.price = purchase_price
        self.plan_creation_type = plan_creation_type
        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token),
                                 ("purchase_price", purchase_price), ("plan_creation_type", plan_creation_type)])
        url = self.url + "NewOnlineOrder".format(
            self.merchant.OpenURLMode)
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    @prepare_response
    def create_online_plan(self, order_id):
        setattr(self, "order_id", order_id)
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
            "JamAddress1": self.res_address_1,
            "JamResSuburb": self.res_suburb,
            "JamResState": self.res_state,
            "JamResPostcode": str(self.res_postcode),
        }
        headers = {'Cache-Control': "no-cache"}
        url = self.handover_url.format(self.merchant.OpenURLMode)

        return {"url": url, "http_method": "GET", "params": querystring, "headers": headers}

    @prepare_response
    def check_payment_capture(self, plan_id):
        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token),
                                 ("plan_iD", plan_id)])
        url = self.url + "OnlineOrderCapturePayment".format(
            self.merchant.OpenURLMode)
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    @prepare_response
    def check_order_status(self, plan_id):
        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token),
                                 ("plan_iD", plan_id)])
        url = self.url + "OnlineOrderStatus".format(
            self.merchant.OpenURLMode)
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    @prepare_response
    def refund_status(self, plan_id, **kwargs):
        new_purchase_price = 0.00 if kwargs.get("full_refund", False) else kwargs["new_purchase_price"]
        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token), ("plan_iD", plan_id),
                                 ("new_purchase_price", new_purchase_price), ("full_refund", kwargs.get("full_refund",
                                                                                                        False))])
        url = self.url + "OnlineOrderReduction".format(
            self.merchant.OpenURLMode)
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    @prepare_response
    def min_max_purchase_price(self):
        jam_auth_token, auth_token = self.merchant.JamAuthToken, self.merchant.AuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("auth_token", auth_token)])
        url = self.url + "MinMaxPurchasePrice".format(
            self.merchant.OpenURLMode)
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}

    def is_valid_price(self, price):
        """
        checking if the price is valid or not for
        payment
        """
        resp = self.min_max_purchase_price()
        if int(resp["status"]) == 0:
            max_price = resp["MaxPrice"]
            min_price = resp["MinPrice"]
            if float(resp["MinPrice"]) <= price <= float(resp["MaxPrice"]):
                return {"status": True, "error": ""}
            return {"status": False, "error": "You purchase price is not under min-max range ({} to {})".format(
                min_price, max_price)}
        return resp

    @prepare_response
    def order_dispatch_plan(self, plan_id):
        jam_auth_token = self.merchant.JamAuthToken
        attr_dict = OrderedDict([("jam_auth_token", jam_auth_token), ("plan_id", plan_id)])
        url = self.url + "OnlineOrderDispatchPlan".format(
            self.merchant.OpenURLMode)
        return {"attr_dict": attr_dict, "url": url, "http_method": "POST"}
