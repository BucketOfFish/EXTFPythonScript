import numpy as np
from Utilities import *

# given aux data lines of 36 bits each, this function extracts hit parameters for tracks
def extractCoordinates(hitCoordinatesData):

    # extracted values
    coordinates = []
    sectorIDs = []
    nTracks = 0

    # control and header words
    readingDataFragment = False
    headerCount = -1
    readingDataWords = False
    trackWordCount = -1
    trackCoordinates = []

    # read through each line of the file
    for lineNumber, line in enumerate(hitCoordinatesData, start=1):

        if headerCount >= 0 and headerCount <= 6:
            headerCount += 1
            if headerCount == 7:
                readingDataWords = True

        if regSlice(line, 31, 16) == '1110000011011010': # e0da
            readingDataWords = False

        if regSlice(line, 31, 16) == '1011000011110000': # b0f0
            readingDataFragment = True
            headerCount = 0

        if regSlice(line, 31, 16) == '1110000011110000': # e0f0
            readingDataFragment = False
            headerCount = -1

        if readingDataWords:

            trackWordCount += 1

            if regSlice(line, 31, 31) == '1': # begin track
                sectorIDs.append('000000' + regSlice(line, 12, 0)) # pad to 18 bits
                nTracks += 1
                trackWordCount = 0
                trackCoordinates = []

            if trackWordCount >= 2 and trackWordCount <= 4: # pixel hit clusters
                columnCoord = regSlice(line, 27, 16)
                rowCoord = regSlice(line, 11, 0)
                trackCoordinates.append(columnCoord)
                trackCoordinates.append(rowCoord)

            if trackWordCount >= 5 and trackWordCount <= 9: # SCT hit clusters
                hit1Coord = regSlice(line, 10, 0)
                trackCoordinates.append(hit1Coord)

            if trackWordCount == 9: # end of track
                coordinates.append(trackCoordinates)

    return (sectorIDs, coordinates)
