"""
    Connect.py

    API wrapper for XTS Connect REST APIs.

    :copyright:
    :license: see LICENSE for details.
"""
import configparser
import json
import logging
from urllib.parse import urljoin 
import requests
from requests.adapters import HTTPAdapter
import Exception as ex

log = logging.getLogger(__name__)


class XTSCommon:
    """
    Base variables class
    """

    def __init__(self, token=None, userID=None, isInvestorClient=None):
        """Initialize the common variables."""
        self.token = token
        self.userID = userID
        #self.isInvestorClient = isInvestorClient


class XTSConnect(XTSCommon):
    """
    The XTS Connect API wrapper class.
    In production, you may initialise a single instance of this class per `api_key`.
    """
    """Get the configurations from config.ini"""
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    # Default root API endpoint. It's possible to
    # override this by passing the `root` parameter during initialisation.
    _default_root_uri = cfg.get('root_url', 'root')
    _default_login_uri = _default_root_uri + "/user/session"
    _default_timeout = 7  # In seconds

    # SSL Flag
    _ssl_flag = cfg.get('SSL', 'disable_ssl')

    # URIs to various calls
    _routes = {
       
        # Market API endpoints
        "marketdata.prefix": "apimarketdata",
        "market.login": "/apibinarymarketdata/auth/login",
        "market.logout": "/apibinarymarketdata/auth/logout",

        "market.config": "/apibinarymarketdata/config/clientConfig",

        "market.instruments.master": "/apibinarymarketdata/instruments/master",
        "market.instruments.subscription": "/apibinarymarketdata/instruments/subscription",
        "market.instruments.unsubscription": "/apibinarymarketdata/instruments/subscription",
        "market.instruments.ohlc": "/apibinarymarketdata/instruments/ohlc",
        "market.instruments.indexlist": "/apibinarymarketdata/instruments/indexlist",
        "market.instruments.quotes": "/apibinarymarketdata/instruments/quotes",

        "market.search.instrumentsbyid": '/apibinarymarketdata/search/instrumentsbyid',
        "market.search.instrumentsbystring": '/apibinarymarketdata/search/instruments',

        "market.instruments.instrument.series": "/apibinarymarketdata/instruments/instrument/series",
        "market.instruments.instrument.equitysymbol": "/apibinarymarketdata/instruments/instrument/symbol",
        "market.instruments.instrument.futuresymbol": "/apibinarymarketdata/instruments/instrument/futureSymbol",
        "market.instruments.instrument.optionsymbol": "/apibinarymarketdata/instruments/instrument/optionsymbol",
        "market.instruments.instrument.optiontype": "/apibinarymarketdata/instruments/instrument/optionType",
        "market.instruments.instrument.expirydate": "/apibinarymarketdata/instruments/instrument/expiryDate"
    }
    def __init__(self,
                 apiKey,
                 secretKey,
                 source,
                 userID,
                 password,
                 root=None,
                 debug=False,
                 timeout=None,
                 pool=None,
                 disable_ssl=_ssl_flag):
        """
        Initialise a new XTS Connect client instance.

        - `api_key` is the key issued to you
        - `token` is the token obtained after the login flow. Pre-login, this will default to None,
        but once you have obtained it, you should persist it in a database or session to pass
        to the XTS Connect class initialisation for subsequent requests.
        - `root` is the API end point root. Unless you explicitly
        want to send API requests to a non-default endpoint, this
        can be ignored.
        - `debug`, if set to True, will serialise and print requests
        and responses to stdout.
        - `timeout` is the time (seconds) for which the API client will wait for
        a request to complete before it fails. Defaults to 7 seconds
        - `pool` is manages request pools. It takes a dict of params accepted by HTTPAdapter
        - `disable_ssl` disables the SSL verification while making a request.
        If set requests won't throw SSLError if its set to custom `root` url without SSL.
        """
        self.debug = debug
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.source = source
        self.disable_ssl = disable_ssl
        self.root = root or self._default_root_uri
        self.timeout = timeout or self._default_timeout
        self.password = password
        self.userID= userID
        super().__init__()

        # Create requests session only if pool exists. Reuse session
        # for every request. Otherwise create session for each request
        if pool:
            self.reqsession = requests.Session()
            reqadapter = requests.adapters.HTTPAdapter(**pool)
            self.reqsession.mount("https://", reqadapter)
        else:
            self.reqsession = requests

        # disable requests SSL warning
        requests.packages.urllib3.disable_warnings()

    def _set_common_variables(self, access_token, userID, isInvestorClient):
        """Set the `access_token` received after a successful authentication."""
        super().__init__(access_token,userID, isInvestorClient)

    def _login_url(self):
        """Get the remote login url to which a user should be redirected to initiate the login flow."""
        return self._default_login_uri


    ########################################################################################################
    # Market data API
    ########################################################################################################

    def marketdata_login(self):
        try:
            #self._set_common_variables(token, userid,False)

            params = {
                "appKey": self.apiKey,
                "secretKey": self.secretKey,
                "source": self.source
            }
            response = self._post("market.login", params)
            print(response['result'])
            if "token" in response['result']:
                print("Token exist")
                self._set_common_variables(response['result']['token'], response['result']['userID'],False)
            return response 
        except Exception as e:
            print("In exce")
           # return response

    def get_config(self):
        try:
            params = {}
            response = self._get('market.config', params)
            return response
        except Exception as e:
            return response['description']

    def get_quote(self, Instruments, xtsMessageCode, publishFormat):
        try:

            params = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode, 'publishFormat': publishFormat}
            response = self._post('market.instruments.quotes', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def send_subscription(self, Instruments, xtsMessageCode):
        try:
            params = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode}
            response = self._post('market.instruments.subscription', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def send_unsubscription(self, Instruments, xtsMessageCode):
        try:
            params = {'instruments': Instruments, 'xtsMessageCode': xtsMessageCode}
            response = self._put('market.instruments.unsubscription', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def get_master(self, exchangeSegmentList):
        try:
            params = {"exchangeSegmentList": exchangeSegmentList}
            response = self._post('market.instruments.master', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def get_ohlc(self, exchangeSegment, exchangeInstrumentID, startTime, endTime, compressionValue):
        try:
            params = {
                'exchangeSegment': exchangeSegment,
                'exchangeInstrumentID': exchangeInstrumentID,
                'startTime': startTime,
                'endTime': endTime,
                'compressionValue': compressionValue}
            response = self._get('market.instruments.ohlc', params)
            return response
        except Exception as e:
            return response['description']

    def get_series(self, exchangeSegment):
        try:
            params = {'exchangeSegment': exchangeSegment}
            response = self._get('market.instruments.instrument.series', params)
            return response
        except Exception as e:
            return response['description']

    def get_equity_symbol(self, exchangeSegment, series, symbol):
        try:

            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol}
            response = self._get('market.instruments.instrument.equitysymbol', params)
            return response
        except Exception as e:
            return response['description']

    def get_expiry_date(self, exchangeSegment, series, symbol):
        try:
            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol}
            response = self._get('market.instruments.instrument.expirydate', params)
            return response
        except Exception as e:
            return response['description']

    def get_future_symbol(self, exchangeSegment, series, symbol, expiryDate):
        try:
            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate}
            response = self._get('market.instruments.instrument.futuresymbol', params)
            return response
        except Exception as e:
            return response['description']

    def get_option_symbol(self, exchangeSegment, series, symbol, expiryDate, optionType, strikePrice):
        try:
            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate,
                      'optionType': optionType, 'strikePrice': strikePrice}
            response = self._get('market.instruments.instrument.optionsymbol', params)
            return response
        except Exception as e:
            return response['description']

    def get_option_type(self, exchangeSegment, series, symbol, expiryDate):
        try:
            params = {'exchangeSegment': exchangeSegment, 'series': series, 'symbol': symbol, 'expiryDate': expiryDate}
            response = self._get('market.instruments.instrument.optiontype', params)
            return response
        except Exception as e:
            return response['description']

    def get_index_list(self, exchangeSegment):
        try:
            params = {'exchangeSegment': exchangeSegment}
            response = self._get('market.instruments.indexlist', params)
            return response
        except Exception as e:
            return response['description']

    def search_by_instrumentid(self, Instruments):
        try:
            params = {'source': self.source, 'instruments': Instruments}
            response = self._post('market.search.instrumentsbyid', json.dumps(params))
            return response
        except Exception as e:
            return response['description']

    def search_by_scriptname(self, searchString):
        try:
            params = {'searchString': searchString}
            response = self._get('market.search.instrumentsbystring', params)
            return response
        except Exception as e:
            return response['description']

    def marketdata_logout(self):
        try:
            params = {}
            response = self._delete('market.logout', params)
            return response
        except Exception as e:
            return response['description']

    ########################################################################################################
    # Common Methods
    ########################################################################################################

    def _get(self, route, params=None):
        """Alias for sending a GET request."""
        return self._request(route, "GET", params)

    def _post(self, route, params=None):
        """Alias for sending a POST request."""
        return self._request(route, "POST", params)

    def _put(self, route, params=None):
        """Alias for sending a PUT request."""
        return self._request(route, "PUT", params)

    def _delete(self, route, params=None):
        """Alias for sending a DELETE request."""
        return self._request(route, "DELETE", params)

    def _request(self, route, method, parameters=None):
        """Make an HTTP request."""
        params = parameters if parameters else {}

        # Form a restful URL
        uri = self._routes[route].format(params)
        url = urljoin(self.root, uri)
        headers = {}
        print(self.token)
        if self.token:
            # set authorization header
            headers.update({'Content-Type': 'application/json', 'Authorization': self.token})

        try:
          
            r = self.reqsession.request(method,
                                        url,
                                        data=params if method in ["POST", "PUT"] else None,
                                        params=params if method in ["GET", "DELETE"] else None,
                                        headers=headers,
                                        verify=not self.disable_ssl)

        except Exception as e:
            raise e

        if self.debug:
            log.debug("Response: {code} {content}".format(code=r.status_code, content=r.content))

        # Validate the content type.
        if "json" in r.headers["content-type"]:
            try:
                data = json.loads(r.content.decode("utf8"))
            except ValueError:
                raise ex.XTSDataException("Couldn't parse the JSON response received from the server: {content}".format(
                    content=r.content))

            # api error
            if data.get("type"):

                if r.status_code == 400 and data["type"] == "error" and data["description"] == "Invalid Token":
                    raise ex.XTSTokenException(data["description"])

                if r.status_code == 400 and data["type"] == "error" and data["description"] == "Bad Request":
                    message = "Description: " + data["description"] + " errors: " + str(data['result']["errors"])
                    raise ex.XTSInputException(str(message))

            return data
        else:
            raise ex.XTSDataException("Unknown Content-Type ({content_type}) with response: ({content})".format(
                content_type=r.headers["content-type"],
                content=r.content))
