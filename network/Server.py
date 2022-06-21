import socket, select
import struct

from network.packet.Packet import Packet

class Server:
    """
    Implements server Socket
    """

    def __init__(self, mcast_grp = '224.1.1.1', mcast_port = 5007):
        self.MCAST_GRP = mcast_grp
        self.MCAST_PORT = mcast_port
        MULTICAST_TTL = 2

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    
    def select(self, onPacketRecv, timeout :float):
        """
        Performs select() & executes function given in onPacketRecv
        on all sockets which have received any packets
        """

        read_sockets, write_sockets, error_sockets = select.select([self.__sock], [], [], timeout)
        
        for sock in read_sockets:
            data, address = sock.recvfrom(10240)
            packet = Packet.fromBytes(data)
            
            if callable(onPacketRecv):
                onPacketRecv(packet, address)

    def recvPacket(self) -> Packet:
        """
        Receives packet & returns corresponding class
        """

        data = self.__sock.recv(10240)
        return Packet.fromBytes(data)
    
    def recvPacketFrom(self):
        """
        Same as recvPacket but also returns address from which it was received
        """

        data, address = self.__sock.recvfrom(10240)
        return Packet.fromBytes(data), address

    def sendPacket(self, packet :Packet):
        """
        Sends packet to the unicast group
        """

        self.__sock.sendto(
            packet.toBytes(),
            (self.MCAST_GRP, self.MCAST_PORT)
        )
    
    def sendPacketTo(self, packet :Packet, address):
        """
        Sends packet to the specified address
        """
        
        self.__sock.sendto(
            packet.toBytes(),
            address
        )
