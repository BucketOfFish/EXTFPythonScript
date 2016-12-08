import numpy as np
from Utilities import *

# given aux data lines of 32 bits each, this function extracts DF hit parameters
def extractDFCoordinates(hitCoordinatesData):

    # extracted values
    globalModuleIDs = []
    coordinates = []

    # control and header words
    headerCount = -1
    readingDataWords = False
    readingIBLHit = False
    newModule = False
    currentModuleID = -1

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

            newModule = (regSlice(line, 31, 31) == '1')

            if newModule: # module info
                if regSlice(line, 15, 15) == '0': # IBL hit
                    readingIBLHit = True
                    currentModuleID = binToInt(regSlice(line, 10, 0))
                else: # SCT hit
                    readingIBLHit = False
                    currentModuleID = binToInt(regSlice(line, 12, 0))

            else: # hits info
                if readingIBLHit:
                    columnCoord = binToInt(regSlice(line, 27, 16))
                    rowCoord = binToInt(regSlice(line, 11, 0))
                    globalModuleIDs.append(currentModuleID)
                    coordinates.append([rowCoord, columnCoord])
                else:
                    hit1 = binToInt(regSlice(line, 10, 0))
                    hit2 = binToInt(regSlice(line, 26, 16))
                    if regSlice(line, 15, 15) == '1': # second hit is empty
                        globalModuleIDs.append(currentModuleID)
                        coordinates.append([hit1])
                    else:
                        globalModuleIDs.append(currentModuleID)
                        coordinates.append([hit1])
                        globalModuleIDs.append(currentModuleID)
                        coordinates.append([hit2])

    return zip(globalModuleIDs, coordinates)
