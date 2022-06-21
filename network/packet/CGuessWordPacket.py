from network.packet.Packet import Packet
import tlv8

class CGuessWordPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'word']
    ]

    def __init__(self, word):
        self.word = word
