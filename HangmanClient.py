#!/usr/bin/env python3

import socket
import struct

from network.packet.Packet import Packet
from network.packet.ServerInfoPacket import ServerInfoPacket

from network.Client import Client

client = Client()

while True:
    [packet, address] = client.recvPacketFrom()

    if isinstance(packet, ServerInfoPacket):
        print("Server name:", packet.serverName, "\tServer IP:", address[0])
