# XTS-SDK-Client Python

This is the XTS Python API Client library , which has both Marketdata and Interactive services.
API Documentation for XTS-MarketData API and XTS-Trading API can be found in the below link.

https://developers.symphonyfintech.in/doc/apimarketdata/

https://developers.symphonyfintech.in/doc/interactive/

## Installation

### Prerequisites

Python 3.8 or above.
Internet Access.

Execute below command:
pip install -r requirements.txt

### Usage
Check the config.ini file, need to add the root url keep source as WEBAPI and disable_ssl as true
```
[user]
source=WEBAPI

[SSL]
disable_ssl=True

[root_url]
root=https://developers.symphonyfintech.in
```

#### Create XT Connect Object

```js
"""API Credentials"""  
APP_KEY = "YOUR_APP_KEY_HERE"
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
XTS_API_BASE_URL = "YOUR_CONNECTION_URL"
broadcastmode = "Full"  #Full, Partial, Binary


"""Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
xt = XTSConnect(APP_KEY, SECRET_KEY, source)
```

#### Login
To login into API call the login service which will return a token. This token will help you to access other services throughout the session.
```js
"""Marketdata Login"""
response = xt.marketdata_login()

"""Interactive Login"""
response = xt.interactive_login()
```

#### Subscribe
To Subscribe to symbol use marketdata API. It returns Subscribe Response object which will contain the tick data like LTP, Open, High etc
```js
"""instruments list"""
instruments = [{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},{'exchangeSegment': 1, 'exchangeInstrumentID': 22}]

"""Send Subscription Request"""
response = xt.send_subscription(
Instruments=instruments,
xtsMessageCode=1502)
```

#### Quotes
Quote service returns Asks, Bids and Touchline
```js
"""instruments list"""
instruments = [
	{'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
	{'exchangeSegment': 1, 'exchangeInstrumentID': 22}]

"""Get Quote Request"""
response = xt.get_quote(
	Instruments=instruments,
	xtsMessageCode=1504,
	publishFormat='JSON')
```


 
 #### Streams and Events
 Events such as TouchLine, MarketDepthData, OpenInterest are received from socket.To get those events XTSAPIMarketdataEvents interface needs to be implemented. 
 Event will be received in the respective overridden methods.
 Following are the event names to properly connect & recieve all the data for Binary Marketdata
 "connect", "disconenct", "joined", "error", "xts-binary-packet"
 ```js
# Callback for connection
def connect(self, headers={}, transports='websocket', namespaces=None, socketio_path='apibinarymarketdata/socket.io',
            verify=False):

    url = self.connection_url
    """Connected to the socket."""
    self.sid.connect(url, headers, transports, namespaces, socketio_path)
    self.sid.wait()
    """Disconnected from the socket."""
    # self.sid.disconnect()

def on_connect(self):
    """Connect from the socket."""
    print('Market Data Socket connected successfully!')

def on_joined(self,data):
    print("Socket joined", data)

def on_error(self,data):
    print("Error in websocket", data)

def on_xts_binary_packet(self, data):
    print("Binary Data",data)
 ```

### Examples
Example code demonstrating how to use XTS Api can be found in 
xts-pythonsdk-binarymarketdata-withbroadcastmode-api-sdk
