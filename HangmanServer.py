#!/usr/bin/env python3

import socket
from network.packet.Packet import Packet
from network.packet.SServerInfo import SServerInfo
from network.packet.CJoin import CJoin
from network.packet.SJoin import SJoin
from network.packet.SNewPlayer import SNewPlayer
import time

from network.Server import Server

serverName = 'GameServer'
server = Server()

while True:
    server.sendPacket(SServerInfo(serverName))

    def onPacketRecv(packet, address):
        if isinstance(packet, CJoin):
            clientUsername = packet.username
            server.sendPacketTo(
                SJoin("", True),
                address
            )
            server.sendPacket(
                SNewPlayer(clientUsername)
            )
    
    server.select(onPacketRecv, 2)
    
    time.sleep(2)
