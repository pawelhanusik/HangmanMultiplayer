from network.packet.Packet import Packet
import tlv8

class SGuessLetterPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'word'],
        [tlv8.DataType.INTEGER, 'remainingLifes']
    ]

    def __init__(self, word :str, remainingLifes :int):
        self.word = word
        self.remainingLifes = remainingLifes
