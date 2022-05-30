#!/usr/bin/env python3

import socket
import struct
import time

from network.packet.Packet import Packet
from network.packet.SServerInfoPacket import SServerInfoPacket
from network.packet.CJoinPacket import CJoinPacket
from network.packet.SJoinPacket import SJoinPacket
from network.packet.SNewPlayerPacket import SNewPlayerPacket

from network.Client import Client

from enum import IntEnum

username = input("Select username: ")
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
        if isinstance(packet, SServerInfoPacket):
            address = recvAddress
            print(
                "Server name:", packet.serverName,
                "\tServer IP:", address
            )

            client.sendPacketTo(CJoinPacket(username), address)
            gameState = GameState.WAITING_FOR_PLAYERS

    elif gameState == GameState.WAITING_FOR_PLAYERS:
        if isinstance(packet, SJoinPacket):
            if not packet.isUsernameAccepted:
                print("Incorrect username! Please try other.")
                gameState = GameState.CONNECTING
            else:
                players = packet.playersList.split("\n")
                print("Players:", players)
            
        elif isinstance(packet, SNewPlayerPacket):
            if packet.username not in players:
                players += [packet.username]
            print("Players:", players)
            
