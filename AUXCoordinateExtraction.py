import numpy as np
from Utilities import *

# given aux data lines of 36 bits each, this function extracts hit parameters for tracks
def extractAUXCoordinates(hitCoordinatesData):

    # extracted values
    coordinates = []
    sectorIDs = []
    nTracks = 0

    # control and header words
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
            headerCount = 0

        if regSlice(line, 31, 16) == '1110000011110000': # e0f0
            headerCount = -1

        if readingDataWords:

            trackWordCount += 1

            if regSlice(line, 31, 31) == '1': # begin track
                sectorID = '000000' + regSlice(line, 12, 0) # pad to 18 bits
                sectorIDs.append(int(sectorID, 2))
                nTracks += 1
                trackWordCount = 0
                trackCoordinates = []

            if trackWordCount >= 2 and trackWordCount <= 4: # pixel hit clusters
                columnCoord = regSlice(line, 27, 16)
                rowCoord = regSlice(line, 11, 0)
                trackCoordinates.append(rowCoord)
                trackCoordinates.append(columnCoord)

            if trackWordCount >= 5 and trackWordCount <= 9: # SCT hit clusters
                hit1Coord = regSlice(line, 10, 0)
                trackCoordinates.append(hit1Coord)

            if trackWordCount == 9: # end of track
                trackCoordinates = [binToInt(num) for num in trackCoordinates]
                coordinates.append(trackCoordinates) # 11 coordinates total - first 6 are pixels (row, col), and last 5 are SCT

    return zip(sectorIDs, coordinates)
