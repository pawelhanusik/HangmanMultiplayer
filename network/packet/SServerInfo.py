from network.packet.Packet import Packet
import tlv8

class SServerInfo(Packet):
    def __init__(self, serverName):
        super().__init__()

        self.serverName = serverName
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "SServerInfo"),
            tlv8.Entry(2, self.serverName)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return SServerInfo(
            dataDecoded.first_by_id(2).data
        )
