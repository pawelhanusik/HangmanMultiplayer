from network.packet.Packet import Packet
import tlv8

class SNewPlayerPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'username']
    ]
    
    def __init__(self, username):
        self.username = username

