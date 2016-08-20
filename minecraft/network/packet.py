from abc import ABC, abstractmethod
from minecraft import datatypes
import utils

class InvalidStateException(Exception):
	def __init__(self, error):
		super().__init__(error)

class Packet(ABC):
	length = None
	packetId = None

	@abstractmethod
	def __init__(self):
		pass


class ClientPacket(Packet):
	@abstractmethod
	def getBytes(self):
		pass

class ServerPacket(Packet):
	pass

class 

class HandshakePacket(ClientPacket):
	packetId = datatypes.VariableInt.fromValue(0x00)

	def __init__(self, protocolVersion, serverAddress, serverPort, nextState):
		self.protocolVersion = datatypes.VariableInt.fromValue(protocolVersion)
		self.serverAddress = datatypes.String.fromValue(serverAddress)
		self.serverPort = datatypes.UnsignedShort.fromValue(serverPort)
		self.nextState = datatypes.VariableInt.fromValue(nextState)

		self.length = datatypes.VariableInt.fromValue(utils.getLength(self.packetId, self.protocolVersion, self.serverAddress, self.serverPort, self.nextState))

		self.bytebuffer = utils.getBytes(self.length, self.packetId, self.protocolVersion, self.serverAddress, self.serverPort, self.nextState)
		# self.bytebuffer = self.length.getBytes() + self.packetId.getBytes() + self.protocolVersion.getBytes() + self.serverAddress.getBytes() + self.serverPort.getBytes() + self.nextState.getBytes()

	def getBytes(self):
		return self.bytebuffer

class LoginStartPacket(ClientPacket):
	packetId = datatypes.VariableInt.fromValue(0x00)

	def __init__(self, username):
		self.username = datatypes.String(username)

		self.length = datatypes.VariableInt.fromValue(utils.getLength(self.packetId, self.username))

		self.bytebuffer = utils.getBytes(self.length, self.packetId, self.username)

	def getBytes(self):
		return self.bytebuffer

class EncryptionRequestPacket(ServerPacket):
	packetId = datatypes.VariableInt.fromValue(0x01)

	def __init__(self, length, bytebuffer):
		self.length = length

		self.serverId = datatypes.String.fromBytes(bytebuffer)
		position = len(self.serverId)
		self.publicKey = datatypes.ByteArray.fromBytes(bytebuffer, position)
		position += len(self.publicKey)
		self.verifyToken = datatypes.ByteArray.fromBytes(bytebuffer, position)

class EncryptionResponsePacket(ClientPacket):
	packetId = datatypes.VariableInt.fromValue(0x01)

	def __init__(self, sharedSecrect, verifyToken):
		self.sharedSecrect = sharedSecrect
		self.verifyToken = verifyToken

		self.length = datatypes.VariableInt.fromValue(utils.getLength(self.packetId, self.sharedSecrect, self.verifyToken))

		self.bytebuffer = utils.getBytes(self.length, self.packetId, self.sharedSecrect, self.verifyToken)

	def getBytes(self):
		return self.bytebuffer

class LoginSuccessPacket(ServerPacket):
	packetId = datatypes.VariableInt.fromValue(0x02)

	def __init__(self, length, bytebuffer):
		self.length = length

		self.uuid = datatypes.String.fromBytes(bytebuffer)
		position += len(self.uuid)
		self.username = datatypes.String.fromBytes(bytebuffer, position)

class JoinGamePacket(ServerPacket):
	packetId = datatypes.VariableInt.fromValue(0x23)

	def __init__(self, length, bytebuffer):
		self.length = length

		self.entityId = datatypes.Int.fromBytes(bytebuffer)
		position = len(self.entityId)
		self.gamemode = datatypes.UnsignedByte.fromBytes(bytebuffer, position)
		position += len(self.gamemode)
		self.dimension = datatypes.Int.fromBytes(bytebuffer, position)
		position += len(self.dimension)
		self.difficulty = datatypes.UnsignedByte.fromBytes(bytebuffer, position)
		position += len(self.difficulty)
		self.maxPlayers = datatypes.UnsignedByte.fromBytes(bytebuffer, position)
		position += len(self.maxPlayers)
		self.levelType = datatypes.String.fromBytes(bytebuffer, position)
		position += len(self.levelType)
		self.reducedDebugInfo = datatypes.Boolean.fromBytes(bytebuffer, position)

class PluginMessagePacket(ServerPacket):
	packetId = datatypes.VariableInt.fromValue(0x18)

	def __init__(self, length, bytebuffer):
		self.length = length

		self.channel = datatypes.String.fromBytes(bytebuffer)
		self.data = datatypes.ByteArray.fromValue(bytebuffer[utils.getLength(self.packetId, self.channel):])

class ServerDifficultyPacket(ServerPacket):
	packetId = datatypes.VariableInt.fromValue(0x0f)

	def __init__(self, length, bytebuffer):
		self.length = length

		self.difficulty = datatypes.UnsignedByte.fromBytes(bytebuffer)

class SpawnPositionPacket(ServerPacket):
	packetId = datatypes.VariableInt.fromValue(0x43)

	def __init__(self, length, bytebuffer):
		self.length = length

		self.location = datatypes.Position.fromBytes(bytebuffer)

class PlayerAbilitiesPacket(ServerPacket):
	packetId = datatypes.VariableInt.fromValue(0x2b)

	def __init__(self, length, bytebuffer):
		self.length = length

		self.flags = datatypes.Byte.fromBytes(bytebuffer)
		position = len(self.flags)
		self.flyingSpeed = datatypes.Float.fromBytes(bytebuffer, position)
		position += len(self.flyingSpeed)
		self.fieldOfViewModifier = datatypes.Float.fromBytes(bytebuffer, position)

class PluginMessageClientPacket(ClientPacket):
	packetId = datatypes.VariableInt.fromValue(0x09)

	def __init__(self, channel, data):
		self.channel = datatypes.String.fromValue(channel)
		self.data = data

		self.length = datatypes.VariableInt.fromValue(utils.getLength(self.packetId, self.channel, self.data))

		self.bytebuffer = utils.getBytes(self.length, self.packetId, self.channel) + self.data

	def getBytes(self):
		return self.bytebuffer

class ClientSettingsPacket(ClientPacket):
	packetId = datatypes.VariableInt.fromValue(0x04)

	def __init__(self, locale, viewDistance, chatMode, chatColors, displayedSkinParts, mainHand):
		self.locale = datatypes.String.fromValue(locale)
		self.viewDistance = datatypes.Byte.fromValue(viewDistance)
		self.chatMode = datatypes.VariableInt.fromValue(chatMode)
		self.chatColors = datatypes.Boolean.fromValue(chatColors)
		self.displayedSkinParts = datatypes.UnsignedByte.fromValue(displayedSkinParts)
		self.mainHand = datatypes.VariableInt.fromValue(mainHand)

		self.length = utils.getLength(self.packetId, self.locale, self.viewDistance, self.chatMode, self.chatColors, self.displayedSkinParts, self.mainHand)

		self.bytebuffer = utils.getBytes(self.length, self.packetId, self.viewDistance, self.chatMode, self.chatColors, self.displayedSkinParts, self.mainHand)

	def getBytes(self):
		return self.bytebuffer