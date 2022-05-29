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

    read_sockets, write_sockets, error_sockets = server.select(2)

    print(
        len(read_sockets),
        len(write_sockets),
        len(error_sockets)
    )

    for sock in read_sockets:
        data, address = sock.recvfrom(10240)
        packet = Packet.fromBytes(data)

        if isinstance(packet, CJoin):
            clientUsername = packet.username
            server.sendPacketTo(
                SJoin("", True),
                address
            )
            server.sendPacket(
                SNewPlayer(clientUsername)
            )
    
    time.sleep(2)
