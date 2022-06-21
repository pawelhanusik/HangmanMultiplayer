from network.packet.Packet import Packet
import tlv8

class SInfoToUser(Packet):
    fields = [
        [tlv8.DataType.STRING, 'info']
    ]
    
    def __init__(self, info):
        self.info = info
