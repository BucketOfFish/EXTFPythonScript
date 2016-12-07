from struct import pack,unpack

# mimics verilog register index slicing behavior
def regSlice(reg, sliceIndex1, sliceIndex2):
    regSize = len(reg)
    return reg[regSize-sliceIndex1-1: regSize-sliceIndex2]

# sets an index in a bit string to be a 0 or a 1
def setBit(bitString, index, value):
    bitStringSize = len(bitString)
    bitString[bitStringSize-index-1] = value

# a series of conversion functions
def hexToBin(hexNumber):
    return bin(int('1'+hexNumber, 16))[3:]
def binToInt(binary):
    return int(binary, 2)
def binToFloat32(binary):
    integer = binToInt(binary)
    return unpack("f", pack("I", integer))[0]
def hexToFloat32(hexNumber):
    binary = hexToBin(hexNumber)
    return binToFloat32(binary)
def hexToInt(hexNumber):
    binary = hexToBin(hexNumber)
    return binToInt(binary)
