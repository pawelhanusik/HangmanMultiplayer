from network.packet.Packet import Packet
import tlv8

class SGuessWordPacket(Packet):
    def __init__(self, isOk :bool, remainingLifes :int):
        super().__init__()

        self.isOk = isOk
        self.remainingLifes = remainingLifes
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "SGuessWordPacket"),
            tlv8.Entry(2, self.isOk),
            tlv8.Entry(3, self.remainingLifes)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.INTEGER,
            3: tlv8.DataType.INTEGER
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return SGuessWordPacket(
            bool(dataDecoded.first_by_id(2).data),
            dataDecoded.first_by_id(3).data
        )
