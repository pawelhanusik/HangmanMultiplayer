#!/usr/bin/env python3

import socket
from network.packet.Packet import Packet
from network.packet.ServerInfoPacket import ServerInfoPacket
import time

from network.Server import Server

serverName = 'GameServer'
server = Server()

while True:
    server.sendPacket(ServerInfoPacket(serverName))
    time.sleep(2)

