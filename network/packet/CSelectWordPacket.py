from network.packet.Packet import Packet
import tlv8

class CSelectWordPacket(Packet):
    def __init__(self, word):
        super().__init__()

        self.word = word
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "CSelectWordPacket"),
            tlv8.Entry(2, self.word)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return CSelectWordPacket(
            dataDecoded.first_by_id(2).data
        )
