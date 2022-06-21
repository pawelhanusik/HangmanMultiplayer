from network.packet.Packet import Packet
import tlv8

class CJoinPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'username']
    ]
    
    def __init__(self, username):
        self.username = username
