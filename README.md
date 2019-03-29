## Python Openpay SDK

This module is created to achieve payment via. [_Openpay_](https://www.openpay.com.au/) from any web based platform 
created by *Python*. Every merchant can use this SDK for its clients to handle order creation to complete payment.  


### Installation

```pip install python-openpay```

### Creation of Merchant
Every _merchant_ object is created by using compulsory attribute **jam_auth_token**, **country_code** and along with other two non-mandatory attributes 
such as - **auth_token** and **openpay_url_mode** as follows:-.
```python
from openpay import Merchant
merchant= Merchant(jam_auth_token='your jam auth token',country_code="au or uk" auth_token=None, openpay_url_mode="Live")
``` 
Here, **openpay_url_mode** is used to specify the mode of URL, such as "_Live_" or "_Training_". This is required for testing this SDK 
in **demo** or **production** purpose. 

Now a _merchant_ can set up _success_, _cancel_ and _failure_ urls for redirecting a client during or after payment through **openpay** 
as follows:-
```python[]
merchant.set_callback_url(callback_url=val1, cancel_url=val2, failure_url=val3)
```
### fraud altert
if any fraud is taking place corresponding to a plan id then merchant can call this following function

```python
merchant.online_order_fraud_alert(plan_id=plan_id)
``` 
**Note:** **This is not mandatory. It will only be called if fraud occurs**

### Creation of Client
A particular **merchant** has a set of **clients** for his site. So, when we create a _client_ object then we have to 
associate a _merchant_ object with it. Possible ways to associate a _client_ with _merchant_ are as follows:-

```python
from openpay import  Client
client = Client(merchant=merchant) # association with merchant
 ```
Later, we can update a _client_ object using **demographic information** as follows(res for residential and del for delivery address):-
 ```python
client(first_name='openpay', family_name='test', email='testdevloper007@gmail.com', res_address_1='15/520 Collins Street',
res_suburb='Melbourne', res_state='Victoria', res_postcode=3000, dob='06 Jan 1985')
```
Add just add del_ suffix like ```del_address_1``` instead of ```res_address_1``` for ```address, suburb and state```.

Another way to create _client_ with two above steps in together as follows :
```python
client = Client(first_name='Test', family_name='User', email='testdevloper007@gmail.com', address_1='15/520 Collins Street',
suburb='Melbourne', state='Victoria', postcode=3000, dob='06 Jan 1985', merchant=merchant)
```
**Note:** Here _```%b```_ *_Month as locale’s abbreviated name. Jan, Feb, …, Dec_*. So, any valid _date format_ should be 
like '**06 Jan 1985**'. In addition, _postal code_ should be of length **4**.  
### Check if price is valid for payment(comes in min max range)
Before initiating order, need to check if price is valid with
```python
client.is_valid_price(price=<payment price>)
```
If the status is True or error is blank in response then we can proceed further with the next call ```new_online_order```
### Online order creation
Here, _client_ is going to order one or more item(s) from _merchant_ site and param _purchase_price_ is the sum of
item(s) prices chosen by client.
```python
client.new_online_order(purchase_price=<total price>, plan_creation_type="Pending")
```
After successful execution, a **plan ID** is created for the _client_.
### Check Min and Max purchase price 
```python
client.min_max_purchase_price()
```
This method is used to check whether the _purchase_price_ is in the **minimum** and **maximum** price range of a
_merchant_ or not.

### Create online plan
```python
plan_link = client.create_online_plan(order_id= <orderID created from merchant site>)
```
Openpay provides all possible plans to pay _purchase_price_ for this _client_. Once a plan is chosen by _client_ then Openpay 
redirects him for payment.

### Check payment and order status
To check payment and order status for a _client_, we should call below functions with **plan_id** as argument respectively.
```python
client.check_payment_capture(plan_id=plan_id)
client.check_order_status(plan_id=plan_id)

```
### Create refund
If _merchant_ wants to create any **partial** refund for a plan then he has to set arguments _plan_id_ and 
_new_purchase_price_ as follows:-

```python
client.refund_status(plan_id=plan_id, new_purchase_price= <revised purchase price>)
```
**Note:** Argument _new_purchase_price_ is calculated as follows:-
```markdown
previous purchase price - amount of price to refund
```

In case of **full** refund, set arguments _plan_id_ and _full_refund_ as follows:-
```python
client.refund_status(plan_id=plan_id, full_return=True)
```

### Create dispatch
If _merchant_ wants to initiate a _dispatch_ of an order then he will following method with corresponding _plan_id_ 
of that order as follows:-
```python
client.order_dispatch_plan(plan_id=plan_id)
```
