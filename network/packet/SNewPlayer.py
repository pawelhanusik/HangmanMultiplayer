from network.packet.Packet import Packet
import tlv8

class SNewPlayer(Packet):
    def __init__(self, username):
        super().__init__()

        self.username = username
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "SNewPlayer"),
            tlv8.Entry(2, self.username)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return SNewPlayer(
            dataDecoded.first_by_id(2).data
        )
