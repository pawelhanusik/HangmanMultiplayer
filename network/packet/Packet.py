import tlv8
import importlib

class Packet:
    """
    Implements packet that can be sent/received by the app.
    
    Conversions from bytes & to bytes are done by this Packet class.
    Other Packet classes only defines fields & variables, based on which
    the correct conversion is done.
    """

    # Definition of fields for a Packet
    fields = []

    def __getClassName(self):
        return self.__class__.__name__

    def toBytes(self):
        """
        Converts packet to bytes that can be sent directly by socket
        """

        structure = [
            tlv8.Entry(1, self.__getClassName())
        ]

        # Fill structure based on fileds defined in the Packet class
        keyId = 2
        for f in self.fields:
            structure += [
                tlv8.Entry(keyId, getattr(self, f[1]), f[0])
            ]
            keyId += 1
        return tlv8.encode(structure)

    @staticmethod
    def fromBytes(data):
        """
        Converts received bytes by socket into Packet instance
        Based on data received, it will automatically choose proper packet class
        """

        if data is None:
            return None

        # Receive class name which packet class is being received
        expected_structure = {
            1: tlv8.DataType.STRING
        }
        
        dataDecoded = tlv8.decode(data, expected_structure)
    
        packetName = dataDecoded.first_by_id(1).data
        
        # Import file with correct Packet class definition
        class_ = getattr(importlib.import_module("network.packet." + packetName), packetName)

        expected_structure = {
            1: tlv8.DataType.STRING
        }

        # Create expected_structure based on fields defined in received packet class
        keyId = 2
        keyIdParamName = {}
        for f in class_.fields:
            expected_structure[keyId] = f[0]
            keyIdParamName[keyId] = f[1]
            keyId += 1
        
        dataDecoded = tlv8.decode(data, expected_structure)
        
        # Prepare arguments for the Packet class from received data
        arguments = {}
        for keyId in keyIdParamName:
            paramName = keyIdParamName[keyId]
            arguments[paramName] = dataDecoded.first_by_id(keyId).data

        # Instantiate the received Packet class
        return class_(**arguments)
