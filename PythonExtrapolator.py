import numpy as np
from MatrixExtraction import *
from CoordinateExtraction import *

if __name__ == "__main__":

    matrixConstantsFileName = 'Data/EXP_T11_21P.txt'
    inputCoordinatesFileName = 'Data/tvec_AUX_tower11_2P40T.txt'

    # open files and read lines
    with open(matrixConstantsFileName) as matrixConstantsFile:
        matrixConstantsData = [line.strip('\n') for line in matrixConstantsFile.readlines()]
    with open(inputCoordinatesFileName) as inputCoordinatesFile:
        inputCoordinatesData = [line.strip('\n') for line in inputCoordinatesFile.readlines()]

    # convert to binary (easier to work with)
    matrixConstantsData = [hexToBin(hexNumber) for hexNumber in matrixConstantsData]
    inputCoordinatesData = [hexToBin(hexNumber) for hexNumber in inputCoordinatesData]

    # get matrices and track coordinates with sector IDs
    matrixValues = extractMatrices(matrixConstantsData)
    hitCoordinates = extractCoordinates(inputCoordinatesData)

    # for every track, compute the extrapolated coordinates
    for hitCoordinateValues in hitCoordinates:

        sectorID = hitCoordinateValues[0]
        coordinates = np.array(hitCoordinateValues[1])

        if sectorID in matrixValues: # if this key is in the dictionary
            vector = np.array(matrixValues[sectorID][0])
            matrix = np.array(matrixValues[sectorID][1])
            print "Track in sector ID", sectorID, "has extrapolated coordinates:", vector + matrix.dot(coordinates)

        else:
            print "Sector ID", sectorID, "is not in matrix data."
