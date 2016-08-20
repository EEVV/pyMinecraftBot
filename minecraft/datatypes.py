from abc import ABC, abstractmethod
import struct

class TypeObject(ABC):
	@classmethod
	@abstractmethod
	def fromBytes(cls, bytebuffer, index = 0):
		pass

	@classmethod
	@abstractmethod
	def fromValue(cls, value):
		pass

	@abstractmethod
	def getBytes(self):
		pass

	@abstractmethod
	def getValue(self):
		pass

	@abstractmethod
	def __len__(self):
		pass

class Boolean(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		boolean = None

		if bytebuffer[index] == 0:
			boolean = False

		if bytebuffer[index] == 1:
			boolean = True

		returnObject = cls()
		returnObject.boolean = boolean
		returnObject.bytebuffer = bytearray(bytebuffer[index].to_bytes(1, "big"))

		return returnObject

	@classmethod
	def fromValue(cls, value):
		bytebuffer = bytearray()

		if value:
			bytebuffer += b"\x01"
		
		if not value:
			bytebuffer += b"\x00"

		returnObject = cls()
		returnObject.boolean = value
		returnObject.bytebuffer = bytebuffer

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.boolean

	def __len__(self):
		return 1

class Byte(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.byte = bytebuffer[index]

		if bytebuffer[index] & 128 > 0:
			returnObject.byte = bytebuffer[index] - 256

		returnObject.bytebuffer = bytearray(bytebuffer[index].to_bytes(1, "big"))

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.byte = value
		returnObject.bytebuffer = value.to_bytes(1, "big", signed = True)

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.byte

	def __len__(self):
		return 1

class UnsignedByte(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.byte = bytebuffer[index]
		returnObject.bytebuffer = bytebuffer[index].to_bytes(1, "big")

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.byte = value
		returnObject.bytebuffer = value.to_bytes(1, "big")

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.byte

	def __len__(self):
		return 1

class Short(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.bytebuffer = bytebuffer[index:index+2]
		returnObject.short = int.from_bytes(returnObject.bytebuffer, "big", signed = True)

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.short = value
		returnObject.bytebuffer = value.to_bytes(2, "big", signed = True)

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.short

	def __len__(self):
		return 2

class UnsignedShort(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.bytebuffer = bytebuffer[index:index+2]
		returnObject.short = int.from_bytes(returnObject.bytebuffer, "big")

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.short = value
		returnObject.bytebuffer = value.to_bytes(2, "big")

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.short

	def __len__(self):
		return 2

class Int(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.bytebuffer = bytebuffer[index:index+4]
		returnObject.integer = int.from_bytes(returnObject.bytebuffer, "big", signed = True)

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.integer = value
		returnObject.bytebuffer = value.to_bytes(4, "big", signed = True)

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.integer

	def __len__(self):
		return 4

class Long(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.bytebuffer = bytebuffer[index:index+8]
		returnObject.long = long.from_bytes(returnObject.bytebuffer, "big")

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.long = value
		returnObject.bytebuffer = value.to_bytes(8, "big")

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.long

	def __len__(self):
		return 8

class Float(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.bytebuffer = bytebuffer[index:index+4]
		returnObject.float = struct.unpack(">f", returnObject.bytebuffer)[0]

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.float = value
		returnObject.bytebuffer = bytearray(struct.pack(">f", value))

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.float

	def __len__(self):
		return 4

class Double(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.bytebuffer = bytebuffer[index:index+8]
		returnObject.double = struct.unpack(">d", returnObject.bytebuffer)[0]

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.double = value
		returnObject.bytebuffer = bytearray(struct.pack(">d", value))

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.double

	def __len__(self):
		return 8

class String(TypeObject):
	@classmethod
	def fromValue(cls, string):
		bytebuffer = string.encode("utf-8")
		length = VariableInt.fromInt(len(bytebuffer))

		returnObject = cls()
		returnObject.bytebuffer = bytebuffer
		returnObject.length = length

		return returnObject

	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		startIndex = index

		length = VariableInt.fromBytes(bytebuffer, index)
		stringBytebuffer = bytearray()

		index += len(length)

		startOfString = index

		while index-startOfString < length.integer:
			stringBytebuffer += bytebuffer[index].to_bytes(1, "big")

			index += 1

		returnObject = cls()
		returnObject.length = length
		returnObject.bytebuffer = stringBytebuffer
		returnObject.string = stringBytebuffer.decode("utf-8")

		return returnObject

	def getBytes(self):
		return self.length.getBytes() + self.bytebuffer

	def getValue(self):
		return self.string

	def __len__(self):
		return len(self.getBytes())

class Chat(TypeObject):
	pass # unsure about this class

class VariableInt(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		startIndex = index

		integer = 0

		position = 0
		while True:
			if index-startIndex == 4:
				break

			byte = bytebuffer[index]

			integer = integer | ((byte & 127) << position)

			position += 7
			index += 1

			if (byte & 128) == 0:
				break

		returnObject = cls()
		returnObject.long = integer
		returnObject.bytebuffer = bytebuffer[startIndex:index]

		return returnObject

	@classmethod
	def fromValue(cls, value):
		firstInteger = value

		bytebuffer = bytearray()

		while value > 127:
			byte = (value & 127) | 128

			bytebuffer += byte.to_bytes(1, "big")

			value = value >> 7

		bytebuffer += value.to_bytes(1, "big")

		returnObject = cls()
		returnObject.long = firstInteger
		returnObject.bytebuffer = bytebuffer

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.integer

	def __len__(self):
		return len(self.bytebuffer)

class VariableLong(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		startIndex = index

		integerLong = 0

		position = 0
		while True:
			if index-startIndex == 9:
				break

			byte = bytebuffer[index]

			integerLong = integerLong | ((byte & 127) << position)

			position += 7
			index += 1

			if (byte & 128) == 0:
				break

		returnObject = cls()
		returnObject.long = integerLong
		returnObject.bytebuffer = bytebuffer[startIndex:index]

		return returnObject

	@classmethod
	def fromValue(cls, value):
		firstIntegerLong = value

		bytebuffer = bytearray()

		while value > 127:
			byte = (value & 127) | 128

			bytebuffer += byte.to_bytes(1, "big")

			value = value >> 7

		bytebuffer += value.to_bytes(1, "big")

		returnObject = cls()
		returnObject.long = firstIntegerLong
		returnObject.bytebuffer = bytebuffer

		return returnObject

	def getBytes(self):
		return self.bytebuffer

	def getValue(self):
		return self.long

	def __len__(self):
		return len(self.bytebuffer)

class ByteArray(TypeObject):
	@classmethod
	def fromBytes(cls, bytebuffer, index = 0):
		returnObject = cls()
		returnObject.length = VariableInt.fromBytes(bytebuffer, index = 0)
		returnObject.bytebuffer = bytebuffer[returnObject.length.getValue():]

		return returnObject

	@classmethod
	def fromValue(cls, value):
		returnObject = cls()
		returnObject.length = VariableInt.fromValue(len(value))
		returnObject.bytebuffer = value

		return returnObject

	def getBytes(self):
		return self.length.getBytes() + self.bytebuffer

	def getValue(self):
		return self.bytebuffer

	def __len__(self):
		return len(self.getBytes())