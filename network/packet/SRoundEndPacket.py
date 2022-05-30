from network.packet.Packet import Packet
import tlv8

class SRoundEndPacket(Packet):
    def __init__(self, scoreboard :str):
        super().__init__()

        self.scoreboard = scoreboard
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "SRoundEndPacket"),
            tlv8.Entry(2, self.scoreboard)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return SRoundEndPacket(
            dataDecoded.first_by_id(2).data
        )
