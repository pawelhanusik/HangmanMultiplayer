from network.packet.Packet import Packet
import tlv8

class CStartGame(Packet):
    def __init__(self):
        super().__init__()
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "CStartGame")
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        return CStartGame()
