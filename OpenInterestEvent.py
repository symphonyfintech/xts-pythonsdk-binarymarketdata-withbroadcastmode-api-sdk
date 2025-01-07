from ApplicationMessageVersion import ApplicationMessageVersion

class OpenInterest:
    @staticmethod
    def deserialize(reader, count, messagecode, broadcastmode):
        count += 2  # Skip initial bytes for flags
        messageVersion = reader.read_uint16()
        applicationType = reader.read_uint16()
        tokenID = reader.read_uint64()
        count += 8

        sequenceNumber, SkipBytes = 0, 0
        if messageVersion >= ApplicationMessageVersion.Version_1_0_1_2983.value:
            sequenceNumber = reader.read_uint64()
            count += 8
            SkipBytes = reader.read_int32()
            count += 4

        exchangeSegment = reader.read_int16()
        count += 2
        exchangeInstrumentId = reader.read_int32()
        count += 4
        exchangeTimestamp = reader.read_uint64()
        count += 8
        MarketType = reader.read_int16()
        count += 2
        openInterest = reader.read_int32()
        count += 4
        underlyingExchangeSegment = reader.read_int16()
        count += 2
        underlyingInstrumentID = reader.read_uint64()
        count += 8
        isStringExits = reader.read_int8()
        count += 1

        if isStringExits == 1:
            stringLength = reader.read_int8()
            count += 1 + stringLength  # Add the string's length to the count

        underlyingTotalOpenInterest = reader.read_int32()
        count += 4

        if broadcastmode == "Full":
            return {
                "MessageCode": messagecode,
                "MessageVersion": messageVersion,
                "ApplicationType": applicationType,
                "TokenID": tokenID,
                "ExchangeSegment": exchangeSegment,
                "ExchangeInstrumentID": exchangeInstrumentId,
                "ExchangeTimeStamp": exchangeTimestamp,
                "XMarketType": MarketType,
                "OpenInterest": openInterest,
                "UnderlyingExchangeSegment": underlyingExchangeSegment,
                "UnderlyingInstrumentID": underlyingInstrumentID,
                "UnderlyingTotalOpenInterest": underlyingTotalOpenInterest,
                "SequenceNumber": sequenceNumber,
            }

        elif broadcastmode == "Partial":
            return (
                f"t:{exchangeSegment}_{exchangeInstrumentId},"
                f"oi:{openInterest},"
                f"mt:{MarketType},"
                f"uex:{underlyingExchangeSegment},"
                f"uid:{underlyingInstrumentID},"
                f"toi:{underlyingTotalOpenInterest}"
            )

        elif broadcastmode != "Binary":
            print("Invalid broadcastmode value provided.")
            return None
