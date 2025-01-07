
import struct
class MarketDeptRowInfo(): 
    size = 0
    rowprice = 0.0
    totalOrders = 0
    backmarketmakerflag = 0
    def __init__(self, reader, count):
        self.reader = reader
        self.count = count

    def deserialize(self):
        size = self.reader.read_int32()
        self.count += 4
        rowprice = struct.unpack('d', self.reader.read_bytes(8))[0]
        self.count += 8
        totalOrders =  self.reader.read_int32()
        self.count += 4
        backmarketmakerflag =  self.reader.read_int16()
        self.count += 2
        return self.count, {"size":size,"rowprice":rowprice, "totalOrders":totalOrders, "backmarketmakerflag":backmarketmakerflag}
    

