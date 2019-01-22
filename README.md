## Python Openpay SDK

This module is created to achieve payment via. [_OpenPay_](https://www.openpay.com.au/) from any web based platform 
created by *Python*. Every merchant can use admit his SDK for his clients to handle order creation to complete payment.  


### Installation

```pip install openpay-py```


### Creation of Merchant and Client
Create object of the Merchant class passing at least "JamAuthToken" . If you are using **Django** then ```settings.py```
is the best place to instantiate the Client

```python
from openpay import  Client, Merchant
merchant= Merchant(jam_auth_token='your jam auth token')
 ```


to set Merchant's success, cancel and failure url call set_call_back_url and to set user's info call the next function
```python
merchant.set_callback_url(callback_url, cancel_url, failure_url)
```

create client aka user in your desired module, send merchant to attach this with client
```python
client = Client(order_id=100, first_name='Abhisek', family_name='Roy', email='testdevloper007@gmail.com', address_1='15/520 Collins Street',
suburb='Melbourne', state='Victoria', postcode=3000, dob='06 Jan 1985', merchant=merchant)
```
Here _```%b```_ *_Month as locale’s abbreviated name. Jan, Feb, …, Dec_*.
 So the date format should be like '**06 Jan 1985**'.
Sending merchant as argument when creating Client object is **strictly required** in the above code, to proceed further.
Call new_online_order method to create new order 
```client.new_online_order(purchase_price, plan_creation_type)```

To create online plan call

```client.create_online_plan()```

To check order capture & order status you should call below function respectively

```python
client.check_payment_capture(plan_id)
client.check_order_status(plan_id)

```
**_Note:_** You will get  plan id from the very first call of ```new_online_order```

To create refund you've to supply plan_id, new_purchase_price(which is previous price - refund price)

```client.refund_status(plan_id, new_purchase_price)```

_In case of full refund, pass ```full_refund=True``` in place of new_purchase_price so the code will be like_

```python
    client.refund_status(plan_id, full_return=True)
```

If you want to give full refund, you just set the full refund to True, There is no need to pass the price,
otherwise just passing the price is fine for partial refund

To check order dispatch plan
```client.order_dispatch_plan(plan_id)```
