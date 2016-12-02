# converts hex to binary, with leading zeros intact
def hexToBin(hexNumber):
    return bin(int('1'+hexNumber, 16))[3:]

# mimics verilog register index slicing behavior
def regSlice(reg, sliceIndex1, sliceIndex2):
    regSize = len(reg)
    return reg[regSize-sliceIndex1-1: regSize-sliceIndex2]

# sets an index in a bit string to be a 0 or a 1
def setBit(bitString, index, value):
    bitStringSize = len(bitString)
    bitString[bitStringSize-index-1] = value
