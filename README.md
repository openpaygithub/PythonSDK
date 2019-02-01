## Python Openpay SDK

This module is created to achieve payment via. [_Openpay_](https://www.openpay.com.au/) from any web based platform 
created by *Python*. Every merchant can use this SDK for its clients to handle order creation to complete payment.  


### Installation

```pip install python-openpay```

### Creation of Merchant
Every _merchant_ object is created using compulsory attribute **jam_auth_token** and along with two non-mandatory attributes 
such as - **auth_token** and **openpay_url_mode**.
```python
from openpay import Merchant
merchant= Merchant(jam_auth_token='your jam auth token', auth_token=None, openpay_url_mode="Live")
``` 
Here, **openpay_url_mode** is used to specify the URL mode as "_Live_" or "_Training_". 


To set Merchant's _success_, _cancel_ and _failure_ url, call ```set_call_back_url()``` as follows:-
```python
merchant.set_callback_url(callback_url=val1, cancel_url=val2, failure_url=val3)
```

### Creation of Client
A particular **merchant** has a set of **clients** for his/her site. So, when we create a _client_ object then we must 
associate it with its corresponding _merchant_ object.

```python
from openpay import  Client
client = Client(merchant=merchant)
 ```
Later, we can also update a _client_ object using demographic information as follows:-
 ```python
client(first_name='openpay', family_name='test', email='testdevloper007@gmail.com', address_1='15/520 Collins Street',suburb='Melbourne', state='Victoria', postcode=3000, dob='06 Jan 1985')
```


Another way to create _client_ is as follows:
```python
client = Client(first_name='Test', family_name='User', email='testdevloper007@gmail.com', address_1='15/520 Collins Street',suburb='Melbourne', state='Victoria', postcode=3000, dob='06 Jan 1985', merchant=merchant)
```
Here _```%b```_ *_Month as locale’s abbreviated name. Jan, Feb, …, Dec_*.
 So the date format should be like '**06 Jan 1985**'.
Sending merchant as argument when creating Client object is **strictly required** in the above code, to proceed further.
Call new_online_order method to create new order 
```
client.new_online_order(purchase_price, plan_creation_type)
```
Before calling online play check the price is valid or not
```python
client.is_valid(purchase=400)
```

If the price is valid, we can create online plan 

```client.create_online_plan(plan_id=plan_id)``` 

The method will return a plan id which will be used to to initiate few other methods.

To check order capture & order status you should call below function respectively

```python
client.check_payment_capture(plan_id=plan_id)
client.check_order_status(plan_id=plan_id)

```
**_Note:_** You will get  plan id from the very first call of ```new_online_order```

To create refund you've to supply plan_id, new_purchase_price(which is previous price - refund price)

```client.refund_status(plan_id, new_purchase_price)```

_In case of full refund, pass ```full_refund=True``` in place of new_purchase_price so the code will be like_

```python
    client.refund_status(plan_id=plan_id, full_return=True)
```

If you want to give full refund, you just set the full refund to True, There is no need to pass the price,
otherwise just passing the price is fine for partial refund
At last
To initiate dispatch order dispatch plan
```client.order_dispatch_plan(plan_id='your plan id')```
