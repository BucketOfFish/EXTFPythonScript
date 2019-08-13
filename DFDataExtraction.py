import Utilities as U


def extractDFData(hitCoordinatesData):
    '''Given DF data lines of 32 bits each, this function extracts DF hit coordinates and
    returns in the form of a list with (global module ID, hit coordinates).'''

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

        if U.regSlice(line, 31, 16) == '1110000011011010':  # e0da
            readingDataWords = False
            yield zip(globalModuleIDs, coordinates)  # return one event
            globalModuleIDs = []
            coordinates = []

        if U.regSlice(line, 31, 16) == '1011000011110000':  # b0f0
            headerCount = 0

        if U.regSlice(line, 31, 16) == '1110000011110000':  # e0f0
            headerCount = -1

        if readingDataWords:

            newModule = (U.regSlice(line, 31, 31) == '1')

            if newModule:  # module info
                if U.regSlice(line, 15, 15) == '0':  # IBL hit
                    readingIBLHit = True
                    currentModuleID = U.binToInt(U.regSlice(line, 10, 0))
                else:  # SCT hit
                    readingIBLHit = False
                    currentModuleID = U.binToInt(U.regSlice(line, 12, 0))

            else:  # hits info
                if readingIBLHit:
                    columnCoord = U.binToInt(U.regSlice(line, 27, 16))
                    rowCoord = U.binToInt(U.regSlice(line, 11, 0))
                    globalModuleIDs.append(currentModuleID)
                    coordinates.append([rowCoord, columnCoord])
                else:
                    hit1 = U.binToInt(U.regSlice(line, 10, 0))
                    hit2 = U.binToInt(U.regSlice(line, 26, 16))
                    if U.regSlice(line, 15, 15) == '1':  # second hit is empty
                        globalModuleIDs.append(currentModuleID)
                        coordinates.append([hit1])
                    else:
                        globalModuleIDs.append(currentModuleID)
                        coordinates.append([hit1])
                        globalModuleIDs.append(currentModuleID)
                        coordinates.append([hit2])
