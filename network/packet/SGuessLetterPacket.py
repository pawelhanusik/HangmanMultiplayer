from network.packet.Packet import Packet
import tlv8

class SGuessLetterPacket(Packet):
    def __init__(self, occurences :int, word :str, remainingLifes :int):
        super().__init__()

        self.occurences = occurences
        self.word = word
        self.remainingLifes = remainingLifes
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "SGuessLetterPacket"),
            tlv8.Entry(2, self.occurences),
            tlv8.Entry(3, self.word),
            tlv8.Entry(4, self.remainingLifes)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.INTEGER,
            3: tlv8.DataType.STRING,
            4: tlv8.DataType.INTEGER
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return SGuessLetterPacket(
            dataDecoded.first_by_id(2).data,
            dataDecoded.first_by_id(3).data,
            dataDecoded.first_by_id(4).data
        )
