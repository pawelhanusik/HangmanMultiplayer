from network.packet.Packet import Packet
import tlv8

class SGuessLetterPacket(Packet):
    fields = [
        [tlv8.DataType.INTEGER, 'occurences'],
        [tlv8.DataType.STRING, 'word'],
        [tlv8.DataType.INTEGER, 'remainingLifes']
    ]

    def __init__(self, occurences :int, word :str, remainingLifes :int):
        self.occurences = occurences
        self.word = word
        self.remainingLifes = remainingLifes
