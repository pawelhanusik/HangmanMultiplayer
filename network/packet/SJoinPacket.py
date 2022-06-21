from network.packet.Packet import Packet
import tlv8

class SJoinPacket(Packet):
    fields = [
        [tlv8.DataType.STRING, 'playersList'],
        [tlv8.DataType.INTEGER, 'isUsernameAccepted']
    ]
    
    def __init__(self, playersList :str, isUsernameAccepted):
        if not isinstance(isUsernameAccepted, bool):
            isUsernameAccepted = bool(isUsernameAccepted)
        
        self.playersList = playersList
        self.isUsernameAccepted = isUsernameAccepted
