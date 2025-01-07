from MarketDepthRowInfo import MarketDeptRowInfo
from ApplicationMessageVersion import ApplicationMessageVersion
import struct
from datetime import datetime

class Touchline():
    def deserialize(reader,count, messagecode, broadcastmode):
        count+= 2
        messageVersion = reader.read_uint16()
        applicationType = reader.read_uint16()
        tokenID = reader.read_uint64()

        count += 8
        if (messageVersion >= ApplicationMessageVersion.Version_1_0_1_2983.value): 
            sequenceNumber =reader.read_uint64()

            count += 8
            SkipBytes = reader.read_int32()
            count += 4

        exchangeSegment = int(reader.read_int16())
        count+= 2

        exchangeInstrumentId = reader.read_int32()
        count+= 4

        exchangeTimestamp = reader.read_uint64()
        count+= 8

        md1 = MarketDeptRowInfo(reader, count)
        count, bidData = md1.deserialize()
        md2 = MarketDeptRowInfo(reader, count)
        count, askData = md2.deserialize()

        lut = reader.read_uint64()
        count += 8

        LTP = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8

        ltq = reader.read_int32()
        count += 4

        totalBuyQuantity = reader.read_uint32()
        count += 4

        totalSellQuantity = reader.read_uint32()
        count += 4

        totalTradedQuantity = reader.read_uint32()
        count += 4
        averageTradedPrice = struct.unpack('d', reader.read_bytes(8))[0]

        count += 8

        lastTradedTime = reader.read_int64()
        count += 8

        percentChange = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8

        open =  struct.unpack('d', reader.read_bytes(8))[0]
        count += 8
        
        high = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8
        
        low = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8
        
        close = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8

        
        totalvaluetraded =  struct.unpack('d', reader.read_bytes(8))[0]
        # print("skiptotalvaluetraded ::",totalvaluetraded)
        count += 8
        bbtotalbuy = reader.read_int16()
        count += 2

        bbtotalsell = reader.read_int16()
        count += 2

        Booktype = reader.read_int16()
        count += 2

        MarketType = reader.read_int16()

        if broadcastmode == "Full":
            return {
                "MessageCode": messagecode,
                "MessageVersion": messageVersion,
                "ApplicationType": applicationType,
                "TokenID": tokenID,
                "ExchangeSegment": exchangeSegment,
                "ExchangeInstrumentID": exchangeInstrumentId,
                "ExchangeTimeStamp": exchangeTimestamp,
                "BookType": Booktype,
                "XMarketType": MarketType,
                "SequenceNumber": sequenceNumber,
                "Touchline": {
                    "LastTradedPrice": LTP,
                    "LastTradedQuantity": ltq,
                    "TotalBuyQuantity": totalBuyQuantity,
                    "TotalSellQuantity": totalSellQuantity,
                    "TotalTradedQuantity": totalTradedQuantity,
                    "AverageTradedPrice": averageTradedPrice,
                    "LastTradedTime": lastTradedTime,
                    "LastUpdateTime": str(datetime.now()),
                    "PercentChange": percentChange,
                    "Open": open,
                    "High": high,
                    "Low": low,
                    "Close": close,
                    "TotalValueTraded": totalvaluetraded,
                    "BuyBackTotalBuy": bbtotalbuy,
                    "BuyBackTotalSell": bbtotalsell,
                    "Bid":bidData,
                    "Ask":askData
                }
            }

        elif broadcastmode == "Partial":
            return (
                f"t:{exchangeSegment}_{exchangeInstrumentId},"
                f"ltp:{LTP},"
                f"ltq:{ltq},"
                f"tb:{totalBuyQuantity},"
                f"ts:{totalSellQuantity},"
                f"v:{totalTradedQuantity},"
                f"ap:{averageTradedPrice},"
                f"ltt:{lastTradedTime},"
                f"lut:{lut},"
                f"pc:{percentChange},"
                f"o:{open},"
                f"h:{high},"
                f"l:{low},"
                f"c:{close},"
                f"vp:{totalvaluetraded},"
                f"ai:{askData["size"]}|{askData["rowprice"]}|{askData["totalOrders"]}|{askData["backmarketmakerflag"]}"
                f"bi:{bidData["size"]}|{bidData["rowprice"]}|{bidData["totalOrders"]}|{bidData["backmarketmakerflag"]}"
            )
       

def convertTuple(tup):
        str = ''.join(tup)
        return str














        



def convertTuple(tup):
    return ''.join(tup)
