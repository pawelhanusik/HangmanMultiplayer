from network.packet.Packet import Packet
import tlv8

class CSelectWord(Packet):
    def __init__(self, word):
        super().__init__()

        self.word = word
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "CSelectWord"),
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

        return CSelectWord(
            dataDecoded.first_by_id(2).data
        )
