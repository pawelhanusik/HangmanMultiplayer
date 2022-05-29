import socket
from network.packet.Packet import Packet
from network.packet.ServerInfoPacket import ServerInfoPacket

class Server:
    def __init__(self, mcast_grp = '224.1.1.1', mcast_port = 5007):
        self.MCAST_GRP = mcast_grp
        self.MCAST_PORT = mcast_port
        MULTICAST_TTL = 2

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    
    def sendPacket(self, packet :Packet):
        self.__sock.sendto(
            packet.toBytes(),
            (self.MCAST_GRP, self.MCAST_PORT)
        )
