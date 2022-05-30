#!/usr/bin/env python3

import socket
from network.packet.Packet import Packet
from network.packet.SServerInfoPacket import SServerInfoPacket
from network.packet.CJoinPacket import CJoinPacket
from network.packet.SJoinPacket import SJoinPacket
from network.packet.SNewPlayerPacket import SNewPlayerPacket
from Game import Game, Player
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

            newPlayer = Player(packet.username, address)
            hasNewPlayerBeenAdded = game.addPlayer(newPlayer)

            if not hasNewPlayerBeenAdded:
                server.sendPacketTo(
                    SJoinPacket('', False),
                    newPlayer.address
                )
            else:
                server.sendPacketTo(
                    SJoinPacket(game.getPlayersStr(), True),
                    newPlayer.address
                )
                server.sendPacket(
                    SNewPlayerPacket(newPlayer.username)
                )
    
    server.select(onPacketRecv, 2)
    
    time.sleep(2)
