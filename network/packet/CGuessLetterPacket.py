from network.packet.Packet import Packet
import tlv8

class CGuessLetterPacket(Packet):
    def __init__(self, letter):
        super().__init__()

        self.letter = letter
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "CGuessLetterPacket"),
            tlv8.Entry(2, self.letter)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return CGuessLetterPacket(
            dataDecoded.first_by_id(2).data
        )
