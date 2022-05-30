from network.packet.Packet import Packet
import tlv8

class SRoundEndPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'scoreboard']
    ]

    def __init__(self, scoreboard :str):
        self.scoreboard = scoreboard
