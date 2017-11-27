from Utilities import binToInt

def readAUX(AUXTrack):
    binTrack = (bin(AUXTrack)[2:])[::-1]
    for i in range(10):
        word = binTrack[i*32:(i+1)*32]
        coord1 = binToInt(word[0:12])
        coord2 = binToInt(word[12:24])
        print "Hit", coord1, coord2
