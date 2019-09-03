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
            runNumber = U.binToInt(U.regSlice(U.hexToBin(runNumber), 30, 0))
        elif headerLine == 7:
            lvl1ID = line
        elif headerLine == 8:
            lvl1ID += line
            lvl1ID = U.binToInt(U.regSlice(U.hexToBin(lvl1ID), 23, 0))
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
            # currentTrackInfo.append(U.hexToInt(line))  # tower number
            continue
        elif trackLine == 4:
            # currentTrackInfo.append(U.hexToBin(line))  # layer map
            continue
        elif trackLine == 5:
            roadNumber = line
        elif trackLine == 6:
            roadNumber += line
            # currentTrackInfo.append(U.hexToInt(roadNumber))
            continue
        elif trackLine == 7:
            currentTrackInfo.append(U.hexToFloat16(line))  # chi2
        elif trackLine == 8:
            currentTrackInfo.append([U.hexToFloat16(line)])  # d0
            # continue
        elif trackLine == 9:
            currentTrackInfo[-1].append(U.hexToFloat16(line))  # z0
            # continue
        elif trackLine == 10:
            currentTrackInfo[-1].append(U.hexToFloat16(line))  # coth
            # continue
        elif trackLine == 11:
            currentTrackInfo[-1].append(U.hexToFloat16(line))  # phi0
            # continue
        elif trackLine == 12:
            currentTrackInfo[-1].append(U.hexToFloat16(line))  # curv
            # continue
        elif trackLine >= 13 and trackLine <= 20:
            if trackLine == 13:
                currentTrackInfo.append([])
            currentTrackInfo[-1].append(U.binToInt(U.regSlice(U.hexToBin(line), 11, 0)))  # hit coordinate
        elif trackLine >= 21 and trackLine <= 28:
            currentTrackInfo[-1].append(U.binToInt(U.regSlice(U.hexToBin(line), 10, 0)))  # hit coordinate
            if trackLine == 28:
                currentTrackInfo[-1][0], currentTrackInfo[-1][1] = currentTrackInfo[-1][1], currentTrackInfo[-1][0]  # swap coordinates to match EXTF emulator format
                currentTrackInfo[-1][2], currentTrackInfo[-1][3] = currentTrackInfo[-1][3], currentTrackInfo[-1][2]  # swap coordinates to match EXTF emulator format
                currentTrackInfo[-1][4], currentTrackInfo[-1][5] = currentTrackInfo[-1][5], currentTrackInfo[-1][4]  # swap coordinates to match EXTF emulator format
                currentTrackInfo[-1][6], currentTrackInfo[-1][7] = currentTrackInfo[-1][7], currentTrackInfo[-1][6]  # swap coordinates to match EXTF emulator format
                trackInfo.append(currentTrackInfo)
                trackLine = 0

for track in trackInfo:
    print(track)
import pdb; pdb.set_trace()  # NOQA
