from network.packet.Packet import Packet
import tlv8

class SJoinPacket(Packet):
    def __init__(self, playersList :str, isUsernameAccepted :bool):
        super().__init__()

        self.playersList = playersList
        self.isUsernameAccepted = isUsernameAccepted
    
    def toBytes(self):
        structure = [
            tlv8.Entry(1, "SJoinPacket"),
            tlv8.Entry(2, self.playersList),
            tlv8.Entry(3, self.isUsernameAccepted)
        ]

        return tlv8.encode(structure)
    
    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING,
            2: tlv8.DataType.STRING,
            3: tlv8.DataType.INTEGER
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)

        return SJoinPacket(
            dataDecoded.first_by_id(2).data,
            bool(dataDecoded.first_by_id(3).data)
        )
