from network.packet.Packet import Packet
import tlv8

class SWordReady(Packet):
    def __init__(self):
        super().__init__()
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "SWordReady")
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        return SWordReady()
