#!/usr/bin/env python3

import socket
from network.packet.Packet import Packet
from network.packet.SServerInfoPacket import SServerInfoPacket
from network.packet.CJoinPacket import CJoinPacket
from network.packet.SJoinPacket import SJoinPacket
from network.packet.SNewPlayerPacket import SNewPlayerPacket
import time

from network.Server import Server

serverName = 'GameServer'
players = []
server = Server()

while True:
    server.sendPacket(SServerInfoPacket(serverName))

    def onPacketRecv(packet, address):
        if isinstance(packet, CJoinPacket):
            global players

            clientUsername = packet.username
            players += [clientUsername]

            server.sendPacketTo(
                SJoinPacket('\n'.join(players), True),
                address
            )
            server.sendPacket(
                SNewPlayerPacket(clientUsername)
            )
    
    server.select(onPacketRecv, 2)
    
    time.sleep(2)
