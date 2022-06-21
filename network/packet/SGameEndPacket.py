from network.packet.Packet import Packet
import tlv8

class SGameEndPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'winners']
    ]

    def __init__(self, winners :str):
        self.winners = winners

