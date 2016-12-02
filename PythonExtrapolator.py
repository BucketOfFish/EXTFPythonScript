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
    extractMatrices(matrixConstantsData)
    extractCoordinates(inputCoordinatesData)
