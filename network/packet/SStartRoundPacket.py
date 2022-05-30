from network.packet.Packet import Packet
import tlv8

class SStartRoundPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'pickerUsername'],
        [tlv8.DataType.STRING, 'scoreboard']
    ]

    def __init__(self, pickerUsername :str, scoreboard :str):
        self.pickerUsername = pickerUsername
        self.scoreboard = isUsernameAccepted
