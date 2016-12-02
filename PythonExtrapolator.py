from MatrixExtraction import *

def extractMatricesFromFile(fileName):

    # open file and read lines
    with open(fileName) as matrixConstantsFile:
        matrixConstantsFileLines = [line.strip('\n') for line in matrixConstantsFile.readlines()]

    # convert to binary (easier to work with)
    matrixConstantsFileLines = [hexToBin(hexNumber) for hexNumber in matrixConstantsFileLines]

    extractMatrix(matrixConstantsFileLines[0:63])

if __name__ == "__main__":

    matrixConstantsFileName = 'Data/EXP_T11_21P.txt'
    inputCoordinatesFileName = 'Data/tvec_AUX_tower11_2P40T.txt'

    extractMatricesFromFile(matrixConstantsFileName)
