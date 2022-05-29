#!/usr/bin/env python3

import socket
import struct
import time

from network.packet.Packet import Packet
from network.packet.SServerInfo import SServerInfo
from network.packet.CJoin import CJoin
from network.packet.SJoin import SJoin
from network.packet.SNewPlayer import SNewPlayer

from network.Client import Client

from enum import IntEnum

username = 'PlayerA'
client = Client()

print("Waiting for server...")

class GameState(IntEnum):
    CONNECTING = 0
    WAITING_FOR_PLAYERS = 1

gameState = GameState.CONNECTING
running = True
address = None
players = []

while running:
    if gameState == GameState.CONNECTING:
        packet, recvAddress = client.recvPacketFrom()
    else:
        packet = client.recvPacket()
    
    if gameState == GameState.CONNECTING:
        if isinstance(packet, SServerInfo):
            address = recvAddress
            print(
                "Server name:", packet.serverName,
                "\tServer IP:", address
            )

            client.sendPacketTo(CJoin(username), address)
            gameState = GameState.WAITING_FOR_PLAYERS

    elif gameState == GameState.WAITING_FOR_PLAYERS:
        if isinstance(packet, SJoin):
            if not packet.isUsernameAccepted:
                print("Incorrect username! Please try other.")
                gameState = GameState.CONNECTING
            else:
                players = packet.players.split("\n")
                print("Players:", players)
            
        elif isinstance(packet, SNewPlayer):
            players += [packet.username]
            print("Players:", players)
            
