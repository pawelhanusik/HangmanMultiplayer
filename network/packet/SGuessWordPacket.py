from network.packet.Packet import Packet
import tlv8

class SGuessWordPacket(Packet):
    fields = [
        [tlv8.DataType.INTEGER, 'isOk'],
        [tlv8.DataType.INTEGER, 'remainingLifes']
    ]

    def __init__(self, isOk, remainingLifes :int):
        if not isinstance(isOk, bool):
            isOk = bool(isOk)
        
        self.isOk = isOk
        self.remainingLifes = remainingLifes
