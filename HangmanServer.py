#!/usr/bin/env python3

import socket
from network.packet.Packet import Packet
from network.packet.SServerInfoPacket import SServerInfoPacket
from network.packet.CJoinPacket import CJoinPacket
from network.packet.SJoinPacket import SJoinPacket
from network.packet.SNewPlayerPacket import SNewPlayerPacket
from Game import Game
import time

from network.Server import Server

serverName = 'GameServer'
game = Game()
server = Server()

while True:
    server.sendPacket(SServerInfoPacket(serverName))

    def onPacketRecv(packet, address):
        if isinstance(packet, CJoinPacket):
            global game

            clientUsername = packet.username
            game.addPlayer(clientUsername)
            
            server.sendPacketTo(
                SJoinPacket('\n'.join(game.getPlayers()), True),
                address
            )
            server.sendPacket(
                SNewPlayerPacket(clientUsername)
            )
    
    server.select(onPacketRecv, 2)
    
    time.sleep(2)
