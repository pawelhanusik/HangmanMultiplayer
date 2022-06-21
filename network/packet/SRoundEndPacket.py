from network.packet.Packet import Packet
import tlv8

class SRoundEndPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'scoreboard'],
        [tlv8.DataType.STRING, 'who_won'],
        [tlv8.DataType.STRING, 'game_word']
    ]

    def __init__(self, scoreboard :str, who_won: str, game_word: str):
        self.scoreboard = scoreboard
        self.who_won = who_won
        self.game_word = game_word

