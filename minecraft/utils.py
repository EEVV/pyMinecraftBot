def getLength(*args):
	totalSum = 0

	for i in args:
		totalSum += args[i]

	return totalSum

def getBytes(*args):
	totalBytes = bytearray()

	for i in args:
		totalBytes += i.getBytes()

	return totalBytes