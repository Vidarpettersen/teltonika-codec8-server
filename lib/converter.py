def convert(h, to):
	h = str(h)
	if to == "toInt8" or to == "toUint8":
		return int(h, 8)
	if to == "toInt16" or to == "toUint16":
		return int(h, 16)
	if to == "toInt32" or to == "toUint32":
		return int(h, 32)
	if to == "to[]byte":
		return bytes.fromhex(h)
	return "0"