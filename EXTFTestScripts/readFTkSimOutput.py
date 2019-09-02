import sys
sys.path.append("..")  # NOQA
import Utilities as U

inputFile = open("../Data/Testvector_20190826/output.txt")
inputFileLines = [line.strip('\n') for line in inputFile.readlines()]

# global values
runNumber = -1
lvl1ID = -1
nTracks = 0
trackInfo = []

# track reading progress
readingHeader = False
readingTracks = False
headerLine = 0
trackLine = 0

# read through each line of the file
for lineNumber, line in enumerate(inputFileLines, start=1):

    if not readingHeader and not readingTracks:
        if line == "b0f0":
            readingHeader = True
        else:
            continue

    # read header
    if readingHeader:
        headerLine += 1
        if headerLine == 5:
            runNumber = line
        elif headerLine == 6:
            runNumber += line
            runNumber = U.hexToInt(runNumber)
        elif headerLine == 7:
            lvl1ID = line
        elif headerLine == 8:
            lvl1ID += line
            lvl1ID = U.hexToInt(lvl1ID)
        elif headerLine == 14:
            readingHeader = False
            readingTracks = True
            continue
        else:
            continue

    # read tracks
    if readingTracks:
        trackLine += 1
        if trackLine == 1:
            currentTrackInfo = []
            if line == "e0da":
                readingTracks = False
            continue
        elif trackLine == 2:
            currentTrackInfo.append(U.hexToInt(line))  # sector number
        elif trackLine == 3:
            currentTrackInfo.append(U.hexToInt(line))  # tower number
        elif trackLine == 4:
            currentTrackInfo.append(U.hexToBin(line))  # layer map
            # continue
        elif trackLine == 5:
            roadNumber = line
        elif trackLine == 6:
            roadNumber += line
            currentTrackInfo.append(U.hexToInt(roadNumber))
        elif trackLine == 7:
            currentTrackInfo.append(U.hexToFloat32(line))  # chi2
        elif trackLine == 8:
            currentTrackInfo.append(U.hexToFloat32(line))  # d0
        elif trackLine == 9:
            currentTrackInfo.append(U.hexToFloat32(line))  # z0
        elif trackLine == 10:
            currentTrackInfo.append(U.hexToFloat32(line))  # coth
        elif trackLine == 11:
            currentTrackInfo.append(U.hexToFloat32(line))  # phi0
        elif trackLine == 12:
            currentTrackInfo.append(U.hexToFloat32(line))  # curv
        elif trackLine >= 13:
            if trackLine == 13:
                currentTrackInfo.append([])
            currentTrackInfo[-1].append(U.hexToInt(line))  # hit coordinate
            if trackLine == 28:
                trackInfo.append(currentTrackInfo)
                trackLine = 0

print(trackInfo)
import pdb; pdb.set_trace()  # NOQA
