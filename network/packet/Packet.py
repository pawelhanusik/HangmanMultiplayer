import tlv8
import importlib

class Packet:
    fields = []

    def __getClassName(self):
        return self.__class__.__name__

    def toBytes(self):
        structure = [
            tlv8.Entry(1, self.__getClassName())
        ]

        keyId = 2
        for f in self.fields:
            structure += [
                tlv8.Entry(keyId, getattr(self, f[1]), f[0])
            ]
            keyId += 1
        return tlv8.encode(structure)

    @staticmethod
    def fromBytes(data):
        expected_structure = {
            1: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)
    
        packetName = dataDecoded.first_by_id(1).data
        
        class_ = getattr(importlib.import_module("network.packet." + packetName), packetName)

        expected_structure = {
            1: tlv8.DataType.STRING
        }

        keyId = 2
        keyIdParamName = {}
        for f in class_.fields:
            expected_structure[keyId] = f[0]
            keyIdParamName[keyId] = f[1]
            keyId += 1
        
        dataDecoded = tlv8.decode(data, expected_structure)
        
        arguments = {}
        for keyId in keyIdParamName:
            paramName = keyIdParamName[keyId]
            arguments[paramName] = dataDecoded.first_by_id(keyId).data

        return class_(**arguments)
