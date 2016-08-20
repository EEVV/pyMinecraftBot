from abc import ABC, abstractmethod


class Packet(ABC):
	packetId = None
	length = None

class ClientPacket(Packet, ABC):
	pass

class ServerPacket(Packet, ABC):