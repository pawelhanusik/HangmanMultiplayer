from network.packet.Packet import Packet
import tlv8

class CGuessLetterPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'letter']
    ]

    def __init__(self, letter):
        self.letter = letter
