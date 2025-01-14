from MarketDepthRowInfo import MarketDeptRowInfo
from ApplicationMessageVersion import ApplicationMessageVersion
import struct
from datetime import datetime

class MarketDepthEvent():
    def deserialize(reader, count, messagecode, broadcastmode):
        count += 2
        messageVersion = reader.read_uint16()
        applicationType = reader.read_uint16()
        tokenID = reader.read_uint64()
        count += 8
        if messageVersion >= ApplicationMessageVersion.Version_1_0_1_2983.value:
            sequenceNumber = reader.read_uint64()
            count += 8
            SkipBytes = reader.read_int32()
            count += 4

        exchangeSegment = int(reader.read_int16())
        count += 2
        exchangeInstrumentId = reader.read_int32()
        count += 4
        exchangeTimestamp = reader.read_uint64()
        count += 8
        bidCount = reader.read_int32()
        count += 4

        bidData = []
        for x in range(0, bidCount):
            md = MarketDeptRowInfo(reader, count)
            count, data = md.deserialize()
            bidData.append(data)
        askCount = reader.read_int32()
        count += 4

        askData = []
        for x in range(0, askCount):
            md = MarketDeptRowInfo(reader, count)
            count, data = md.deserialize()
            askData.append(data)
        
        md = MarketDeptRowInfo(reader, count)
        count = md.deserialize()[0]
        md1 = MarketDeptRowInfo(reader, count)
        count = md1.deserialize()[0]
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
        open = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8
        high = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8
        low = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8
        close = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8
        totalValueTraded = struct.unpack('d', reader.read_bytes(8))[0]
        count += 8
        bbTotalBuy = reader.read_int16()
        count += 2
        bbTotalSell = reader.read_int16()
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
                "Ask":askData,
                "Bid":bidData,
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
                    "TotalValueTraded": totalValueTraded,
                    "BuyBackTotalBuy": bbTotalBuy,
                    "BuyBackTotalSell": bbTotalSell
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
                f"vp:{totalValueTraded},"
                f"ai: {askData[0]["size"]}|{askData[0]["rowprice"]}|{askData[0]["totalOrders"]}|{askData[0]["backmarketmakerflag"]}|{askData[1]["size"]}|{askData[1]["rowprice"]}|{askData[1]["totalOrders"]}|{askData[1]["backmarketmakerflag"]}{askData[2]["size"]}|{askData[2]["rowprice"]}|{askData[2]["totalOrders"]}|{askData[2]["backmarketmakerflag"]}|{askData[3]["size"]}|{askData[3]["rowprice"]}|{askData[3]["totalOrders"]}|{askData[3]["backmarketmakerflag"]}|{askData[4]["size"]}|{askData[4]["rowprice"]}|{askData[4]["totalOrders"]}|{askData[4]["backmarketmakerflag"]}"
                f"bi: {bidData[0]["size"]}|{bidData[0]["rowprice"]}|{bidData[0]["totalOrders"]}|{bidData[0]["backmarketmakerflag"]}|{bidData[1]["size"]}|{bidData[1]["rowprice"]}|{bidData[1]["totalOrders"]}|{bidData[1]["backmarketmakerflag"]}{bidData[2]["size"]}|{bidData[2]["rowprice"]}|{bidData[2]["totalOrders"]}|{bidData[2]["backmarketmakerflag"]}|{bidData[3]["size"]}|{bidData[3]["rowprice"]}|{bidData[3]["totalOrders"]}|{bidData[3]["backmarketmakerflag"]}|{bidData[4]["size"]}|{bidData[4]["rowprice"]}|{bidData[4]["totalOrders"]}|{bidData[4]["backmarketmakerflag"]}"
            )



