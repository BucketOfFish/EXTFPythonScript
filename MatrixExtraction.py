import numpy as np
from Utilities import *

# given 64 lines of 32 bits each, this function extracts a vector, a matrix, and other info such as module IDs
# called by PythonExtrapolator.py
def extractMatrix(matrixConstantsData):

    # extracted values
    matrix = []
    vector = []
    emptyID = list('000000000000000000') # some stupid Python nonsense - strings are immutable
    moduleIDs = [list(emptyID), list(emptyID), list(emptyID), list(emptyID), list(emptyID)]
    sectorID = [] # the fifth element of moduleIDs is the sector ID - will be separated at the end
    sectorID_8L = []
    connID = []
    nConn = []

    # read through each line of the file
    for lineNumber, line in enumerate(matrixConstantsData, start=1):

        # first line is 8L sector ID and conn ID
        if lineNumber == 1:
            sectorID_8L = int(regSlice(line, 29, 2), 2)
            connID = regSlice(line, 1, 0)

        elif lineNumber <= 61:
            # these lines contain constants
            matrixConstant = regSlice(line, 26, 0) + '00000'
            matrix.append(binToFloat32(matrixConstant))

            # this line contains n conn
            if lineNumber == 52:
                nConn = regSlice(line, 29, 28)

            # these lines contain module IDs
            if lineNumber <= 50 and (lineNumber-1) % 10 != 0:
                moduleNumber = (lineNumber - 1) // 10
                IDIndex = (lineNumber - 1) % 10
                alteredID = moduleIDs[moduleNumber]
                setBit(alteredID, IDIndex*2-1, regSlice(line, 29, 29))
                setBit(alteredID, IDIndex*2-2, regSlice(line, 28, 28))
                moduleIDs[moduleNumber] = alteredID

    # cleaning up
    moduleIDs = [int(''.join(ID), 2) for ID in moduleIDs]
    sectorID = moduleIDs.pop(4)
    vectorIndexes = [1, 13, 25, 37, 49]
    for index in sorted(vectorIndexes, reverse=True):
        vector.append(matrix.pop(index-1))
    vector = list(reversed(vector))
    matrix = np.array(matrix).reshape(5, 11)

    # return sector ID, vector, and matrix
    return (sectorID_8L, vector, matrix) # the other sectorID is for TF?

def extractMatrices(matrixConstantsData):

    sectorIDs = []
    vectors = []
    matrices = []

    nLines = len(matrixConstantsData)
    nMatrices = 0

    while (nMatrices+1)*64 <= nLines:
        sectorID, vector, matrix = extractMatrix(matrixConstantsData[nMatrices*64:nMatrices*64+63])
        sectorIDs.append(sectorID)
        vectors.append(vector)
        matrices.append(matrix)
        nMatrices += 1
 
    return dict(zip(sectorIDs, zip(vectors, matrices))) # dictionary where sector IDs are keys
