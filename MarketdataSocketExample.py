from datetime import datetime
from Connect import XTSConnect
from Connect import XTSCommon
import configparser
import os
from datetime import datetime
import socketio
from TouchlineEvent import Touchline
from MarketDepthEvent import MarketDepthEvent
from OpenInterestEvent import OpenInterest
from binary_reader import BinaryReader
import zlib


API_KEY = ""
API_SECRET = ""
source = "WEBAPI"
broadcastmode = "Full"  #Full, Partial, Binary


b = bytearray()
xt = XTSConnect(API_KEY, API_SECRET, source,"","")


response = xt.marketdata_login()
print("Login Response -->", response)

set_marketDataToken = response['result']['token']
set_muserID = response['result']['userID'] 

Instruments = [ {'exchangeSegment':1, 'exchangeInstrumentID': 2885}]
subresponse = xt.send_subscription(Instruments, 1501)
print("Subscribe Response -->", subresponse)


class MDSocket_io(socketio.Client):

    def __init__(self, token, userID,broadcastmode, reconnection=False, reconnection_attempts=0, reconnection_delay=1,
                 reconnection_delay_max=50000, randomization_factor=0.5, logger=False, binary=False, json=None,
                 **kwargs):
        self.sid = socketio.Client(logger=False, engineio_logger=False,ssl_verify=False)
        self.eventlistener = self.sid
        self.broadcastMode = broadcastmode
        self.sid.on('connect', self.on_connect)
        self.sid.on('message', self.on_message)
        self.sid.on('error', self.on_error)
        self.sid.on('joined', self.on_joined)
        self.sid.on('xts-binary-packet', self.on_xts_binary_packet)
        self.sid.on('disconnect', self.on_disconnect)

        """Get the root url from config file"""
        currDirMain = os.getcwd()
        configParser = configparser.ConfigParser()
        configFilePath = os.path.join(currDirMain, 'config.ini')
        configParser.read(configFilePath)

        self.port = configParser.get('root_url', 'root')
        self.userID = userID
        publishFormat = 'JSON'
        self.token = token
        print("11111",self.token)
        port = f'{self.port}?token='

        self.connection_url = port + token + '&userID=' + self.userID + '&publishFormat=' + publishFormat + '&broadcastMode=Full'
        print('self.connection_url', self.connection_url)
        
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

    def on_message(self, data):
        """On receiving message"""
        print('I received a message!' + data)
    
    def pako_inflate_raw(self, data):
        decompress = zlib.decompressobj(-15)
        decompressed_data = decompress.decompress(data)
        decompressed_data += decompress.flush()
        return decompressed_data

    def on_xts_binary_packet(self, data):
        try:
            if self.broadcastMode not in ["Binary","Full","Partial"]:
                print("Pass correct broadcastmode value")
                pass

            elif self.broadcastMode == "Binary":
                print("Binary data-->", data)

            else:
                # print("Binary Data1-->",data)
                a = bytearray(data)   
                offset = 0
                count = 0
                currentsize = 0
                isnextpacket = True
                datalen=len(a)
                packetcount = 0
                br = BinaryReader(data)
                packetSize = 0
                uncompressedPacketSize = 0
                nextdata = a
                while (isnextpacket): 
                    nextdata = a[offset:datalen]
                    br = BinaryReader(nextdata)
                    isGzipCompressed = br.read_int8()
                    offset=offset+1
                    if (isGzipCompressed == 1): 
                        nextdata = a[offset:datalen]
                        br = BinaryReader(nextdata)
                        messageCode = br.read_uint16()
                        exchangeSegment = br.read_int16()
                        exchangeInstrumentID = br.read_int32()
                        bookType = br.read_int16()
                        marketType = br.read_int16()
                        uncompressedPacketSize = br.read_uint16()
                        compressedPacketSize = br.read_uint16()
                        offset += 16
                        filteredByteArray = a[offset:(offset + compressedPacketSize)]
                        inflate = self.pako_inflate_raw(filteredByteArray)
                        result = bytearray(inflate)
                        r = BinaryReader(result)
                        currentsize = compressedPacketSize  + offset
                        if (currentsize < len(a)): 
                            isnextpacket = True
                            packetcount = 1
                            offset = currentsize
                        else: isnextpacket = False
                        messageCode = str(r.read_uint16())
                        if ("1501" in str(messageCode)) :
                            touchlineData = Touchline.deserialize(r,count,messageCode,self.broadcastMode)
                            print(touchlineData)
                        elif ("1502" in str(messageCode)):
                            marketDepthdata = MarketDepthEvent.deserialize(r,count,messageCode,self.broadcastMode)
                            print(marketDepthdata)
                        elif ("1510" in str(messageCode)):
                            oidata = OpenInterest.deserialize(r,count,messageCode,self.broadcastMode)
                            print(oidata)

                        # elif ("1512" in messageCode):
                        #     LTPEvent.deserialize(r,count)
                    elif (isGzipCompressed == 0): 
                        messageCode = str(br.read_uint16())
                        exchangeSegment = br.read_int16()
                        exchangeInstrumentID = br.read_int32()
                        bookType = br.read_int16()
                        marketType = br.read_int16()
                        uncompressedPacketSize = br.read_uint16()
                        compressedPacketSize = br.read_uint16()
                        offset += 14
                        count = offset                
                        if ("1501" in messageCode) :
                            touchlineData = Touchline.deserialize(br,count,messageCode,self.broadcastMode)
                            print(touchlineData)
                        elif ("1502" in messageCode):
                            marketDepthdata = MarketDepthEvent.deserialize(br,count,messageCode,self.broadcastMode)
                            print(marketDepthdata)
                        elif ("1510" in messageCode):
                            oidata = OpenInterest.deserialize(br,count,messageCode,self.broadcastMode)
                            print(oidata)

                        currentsize = offset+ uncompressedPacketSize  
                        if (currentsize < len(a)): 
                            isnextpacket = True
                            packetcount = 1
                            offset = currentsize 
                        else: 
                            isnextpacket = False
        except Exception as e:
            print(e)
        

    def on_disconnect(self):
        """Disconnected from the socket"""
        print('Market Data Socket disconnected!')

    def on_error(self, data):
        """Error from the socket"""
        print('Market Data Error', data)


soc = MDSocket_io(set_marketDataToken, set_muserID, broadcastmode)
soc.connect()
