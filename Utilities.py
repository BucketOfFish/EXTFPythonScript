from struct import pack,unpack
import numpy as np
import sys

# mimics verilog register index slicing behavior
# regSlice(reg, a, b) has b as the lower number - takes slice from indices b to a inclusive
def regSlice(reg, sliceIndex1, sliceIndex2):
    regSize = len(reg)
    return reg[regSize-sliceIndex1-1: regSize-sliceIndex2]

# sets an index in a bit string to be a 0 or a 1
def setBit(bitString, index, value):
    bitStringSize = len(bitString)
    bitString[bitStringSize-index-1] = value

# a series of conversion functions - all hex convertions assume 32-bit hex
def hexToBin(hexNumber):
    return bin(int('1'+hexNumber, 16))[3:]
def hexToInt(hexNumber):
    binary = hexToBin(hexNumber)
    return binToInt(binary)
def hexToFloat32(hexNumber):
    binary = hexToBin(hexNumber)
    return binToFloat32(binary)
def hexToFloat16(hexNumber):
    binary = hexToBin(hexNumber)
    return binToFloat16(binary)
def binToInt(binary):
    return int(binary, 2)
def binToHex(binary):
    return hex(int(binary, 2))
def binToFloat32(binary):
    # IEEE-754, but with the first 5 bits removed for some reason when reading TF consts - just following what Markus has in the documentation spreadsheet
    return unpack("f", pack("I", binToInt(binary)))[0]
def binToFloat16(binary):
    return np.frombuffer(pack("H", binToInt(binary)), dtype=np.float16)[0]

# move the first bit of a hex string to the back, or vice versa
def shiftFrontToBack(hexNumber):
    return hexNumber[1:]+hexNumber[0]
def shiftBackToFront(hexNumber):
    return hexNumber[8]+hexNumber[:8] # this is hard-coded, because sometimes there's whitespace at the end of a line, ugh
