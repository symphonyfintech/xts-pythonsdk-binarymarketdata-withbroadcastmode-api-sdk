# from XTConnect import XTSConnect
from Connect import XTSConnect

# logging.basicConfig(level=logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------------------
# Marketdata
# ----------------------------------------------------------------------------------------------------------------------

# Marketdata API Credentials
API_KEY = "YOUR_API_KEY_HERE"
API_SECRET = "YOUR_API_SECRET_HERE"
XTS_API_BASE_URL = "https://xts-api.trading"
source = "WEBAPI"

"""Dealer login credentials"""
API_KEY = "22f6f9dad2fe3982419756"
API_SECRET = "Bxtj027$Dr"
XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
source = "WEBAPI"

"""Investor client login credentials"""
API_KEY = "76179cbae91810ddda7774"
API_SECRET = "Bylg203#fv"
XTS_API_BASE_URL = "https://developers.symphonyfintech.in"
source = "WEBAPI"

"""Make the XTSConnect Object with Marketdata API appKey, secretKey and source"""
xt = XTSConnect(API_KEY, API_SECRET, source)

"""Using the object we call the login function Request"""
response = xt.marketdata_login()
print("MarketData Login: ", response)

"""Get Config Request"""
response = xt.get_config()
print('Config :', response)

"""instruments list"""
instruments = [
    {'exchangeSegment': 1, 'exchangeInstrumentID': 2885},
    {'exchangeSegment': 1, 'exchangeInstrumentID': 22}]

"""Get Quote Request"""
response = xt.get_quote(
    Instruments=instruments,
    xtsMessageCode=1504,
    publishFormat='JSON')
print('Quote :', response)

"""Send Subscription Request"""
response = xt.send_subscription(
    Instruments=instruments,
    xtsMessageCode=1502)
print('Subscribe :', response)

"""Send Unsubscription Request"""
response = xt.send_unsubscription(
    Instruments=instruments,
    xtsMessageCode=1502)
print('Unsubscribe :', response)

"""Get Master Instruments Request"""
exchangesegments = [xt.EXCHANGE_NSECM, xt.EXCHANGE_NSEFO]
response = xt.get_master(exchangeSegmentList=exchangesegments)
print("Master: " + str(response))

"""Get OHLC Request"""
response = xt.get_ohlc(
    exchangeSegment=xt.EXCHANGE_NSECM,
    exchangeInstrumentID=22,
    startTime='Dec 16 2019 090000',
    endTime='Dec 18 2019 150000',
    compressionValue=1)
print("OHLC: " + str(response))

"""Get Series Request"""
response = xt.get_series(exchangeSegment=1)
print('Series:', str(response))

"""Get Equity Symbol Request"""
response = xt.get_equity_symbol(
    exchangeSegment=1,
    series='EQ',
    symbol='Acc')
print('Equity Symbol:', str(response))

"""Get Expiry Date Request"""
response = xt.get_expiry_date(
    exchangeSegment=2,
    series='FUTIDX',
    symbol='NIFTY')
print('Expiry Date:', str(response))

"""Get Future Symbol Request"""
response = xt.get_future_symbol(
    exchangeSegment=2,
    series='FUTIDX',
    symbol='NIFTY',
    expiryDate='28MAY25JUN')
print('Future Symbol:', str(response))

"""Get Option Symbol Request"""
response = xt.get_option_symbol(
    exchangeSegment=2,
    series='OPTIDX',
    symbol='NIFTY',
    expiryDate='26Mar2020',
    optionType='CE',
    strikePrice=10000)
print('Option Symbol:', str(response))

"""Get Option Type Request"""
response = xt.get_option_type(
    exchangeSegment=2,
    series='OPTIDX',
    symbol='NIFTY',
    expiryDate='26Mar2020')
print('Option Type:', str(response))

"""Get Index List Request"""
response = xt.get_index_list(exchangeSegment=xt.EXCHANGE_NSECM)
print('Index List:', str(response))

"""Search Instrument by ID Request"""
response = xt.search_by_instrumentid(Instruments=instruments)
print('Search By Instrument ID:', str(response))

"""Search Instrument by Scriptname Request"""
response = xt.search_by_scriptname(searchString='REL')
print('Search By Symbol :', str(response))

"""Marketdata Logout Request"""
response = xt.marketdata_logout()
print('Marketdata Logout :', str(response))
