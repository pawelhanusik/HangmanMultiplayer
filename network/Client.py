import socket
import struct

from network.packet.Packet import Packet
from network.packet.ServerInfoPacket import ServerInfoPacket

class Client:
    def __init__(self, mcast_grp = '224.1.1.1', mcast_port = 5007):
        self.MCAST_GRP = mcast_grp
        self.MCAST_PORT = mcast_port

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.__sock.bind((self.MCAST_GRP, self.MCAST_PORT))

        mreq = struct.pack("4sl", socket.inet_aton(self.MCAST_GRP), socket.INADDR_ANY)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    def recvPacket(self) -> Packet:
        data = self.__sock.recv(10240)
        return Packet.fromBytes(data)

    def recvPacketFrom(self):
        data, address = self.__sock.recvfrom(10240)
        return Packet.fromBytes(data), address
