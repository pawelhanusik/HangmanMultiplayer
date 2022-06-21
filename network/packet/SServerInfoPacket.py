from network.packet.Packet import Packet
import tlv8

class SServerInfoPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'serverName']
    ]
    
    def __init__(self, serverName):
        self.serverName = serverName
