from network.packet.Packet import Packet
import tlv8

class SStartRoundPacket(Packet):
    def __init__(self, pickerUsername :str, scoreboard :str):
        super().__init__()

        self.pickerUsername = pickerUsername
        self.scoreboard = isUsernameAccepted
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "SStartRoundPacket"),
            tlv8.Entry(2, self.pickerUsername),
            tlv8.Entry(3, self.scoreboard)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.STRING,
            3: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return SStartRoundPacket(
            dataDecoded.first_by_id(2).data,
            dataDecoded.first_by_id(3).data
        )
