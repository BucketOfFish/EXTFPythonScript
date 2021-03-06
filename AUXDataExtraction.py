import Utilities as U


def extractAUXData(inputAUXData_Lines):
    '''Given AUX data lines of 36 bits each, this function extracts hit coordinates for tracks and
    returns in the form of a list with (sectorID, 11 hit coordinates).'''

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
    for lineNumber, line in enumerate(inputAUXData_Lines, start=1):

        if headerCount >= 0 and headerCount <= 6:
            headerCount += 1
            if headerCount == 7:
                readingDataWords = True

        if U.regSlice(line, 31, 16) == '1110000011011010':  # e0da
            readingDataWords = False
            AUXData = zip(sectorIDs, coordinates)
            yield AUXData  # return one event
            sectorIDs = []
            coordinates = []

        if U.regSlice(line, 31, 16) == '1011000011110000':  # b0f0
            headerCount = 0

        if U.regSlice(line, 31, 16) == '1110000011110000':  # e0f0
            headerCount = -1

        if readingDataWords:

            trackWordCount += 1

            if U.regSlice(line, 31, 31) == '1':  # begin track
                # sectorID = U.regSlice(line, 12, 0) + '00'
                sectorID = U.regSlice(line, 15, 0)
                sectorIDs.append(int(sectorID, 2))
                nTracks += 1
                trackWordCount = 0
                trackCoordinates = []

            if trackWordCount >= 2 and trackWordCount <= 4:  # pixel hit clusters
                columnCoord = U.regSlice(line, 27, 16)
                rowCoord = U.regSlice(line, 11, 0)
                trackCoordinates.append(rowCoord)
                trackCoordinates.append(columnCoord)

            if trackWordCount >= 5 and trackWordCount <= 9:  # SCT hit clusters
                hit1Coord = U.regSlice(line, 10, 0)
                trackCoordinates.append(hit1Coord)

            if trackWordCount == 9:  # end of track
                trackCoordinates = [U.binToInt(num) for num in trackCoordinates]
                coordinates.append(trackCoordinates)  # 11 coordinates total - first 6 are pixels (row, col), and last 5 are SCT
