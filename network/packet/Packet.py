import tlv8
import importlib

class Packet:
    def __init__(self):
        pass

    def toBytes(self):
        pass

    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)
    
        packetName = dataDecoded.first_by_id(1).data
        
        class_ = getattr(importlib.import_module("network.packet." + packetName), packetName)
        packet = class_.fromBytes(data)

        return packet

