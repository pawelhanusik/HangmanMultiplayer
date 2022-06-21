from network.packet.Packet import Packet
import tlv8

class CStartGamePacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'start']
    ]
    def __init__(self, start="start"):
        self.start = start
        pass
