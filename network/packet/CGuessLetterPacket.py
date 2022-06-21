from network.packet.Packet import Packet
import tlv8

class CGuessLetterPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'letter'],
        [tlv8.DataType.STRING, 'username']
    ]

    def __init__(self, letter, username):
        self.letter = letter
        self.username = username
