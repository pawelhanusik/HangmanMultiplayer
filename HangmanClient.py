#!/usr/bin/env python3

import socket
import struct
import time

from network.packet.Packet import Packet
from network.packet.SServerInfo import SServerInfo
from network.packet.CJoin import CJoin

from network.Client import Client

username = 'PlayerA'
client = Client()

print("Waiting for server...")

while True:
    packet, address = client.recvPacketFrom()
    
    if isinstance(packet, SServerInfo):
        print(
            "Server name:", packet.serverName,
            "\tServer IP:", address
        )
        break

client.sendPacketTo(CJoin(username), address)
