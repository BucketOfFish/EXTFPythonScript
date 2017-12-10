from Utilities import binToInt, binToHex, regSlice
from __future__ import print_function

def readAUX(AUXTrack):
    AUXTrack = pow(2,320) + AUXTrack
    binTrack = bin(AUXTrack)[len(bin(AUXTrack))-320:]
    for i in range(8):
        word = binTrack[i*32:(i+1)*32]
        coord1 = binToInt(regSlice(word, 11, 0))
        coord2 = binToInt(regSlice(word, 27, 16))
        print("("+str(coord1)+", "+str(coord2)+")", end='')
    print("")

def readDF(DFHit):
    binHit = bin(DFHit)[len(bin(DFHit))-29:]
    reading_module = 0
    if (len(binHit)==31):
        reading_module =  binHit[31]
    is_SCT = binHit[15]
    if (reading_module):
        print "Is module ID"
    else:
        if (is_SCT):
            print "SCT:", binToInt(regSlice(binHit, 10, 0)), binToInt(regSlice(binHit, 26, 16))
        else:
            print "IBL:", binToInt(regSlice(binHit, 11, 0)), binToInt(regSlice(binHit, 27, 16))
