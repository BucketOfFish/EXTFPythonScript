import numpy as np
from Utilities import *

# given 64 lines of 32 bits each, this function extracts a vector, a matrix, and other info such as module IDs
# the return form is a dictionary with sector IDs as keys, and values as (vector, matrix, list of 4 global module IDs)
def extractOneSetOfConstants(extrapolatorConstants_Lines):

    # extracted values
    matrix = []
    vector = []
    emptyID = list('000000000000000000') # some stupid Python nonsense - strings are immutable
    globalModuleIDs = [list(emptyID), list(emptyID), list(emptyID), list(emptyID), list(emptyID)]
    sectorID = [] # the fifth element of globalModuleIDs is the sector ID - will be separated at the end
    sectorID_8L = []
    connID = []
    nConn = []

    # read through each line of the file
    for lineNumber, line in enumerate(extrapolatorConstants_Lines, start=1):

        # first line is 8L sector ID and conn ID
        if lineNumber == 1:
            # sectorID_8L = int(regSlice(line, 29, 2), 2)
            sectorID_8L = int(regSlice(line, 27, 0), 2)
            connID = regSlice(line, 1, 0)

        elif lineNumber <= 61:
            # these lines contain constants
            matrixConstant = regSlice(line, 26, 0) + '00000' # strip off the first bits and put them at the end - just dumb formatting for changing from 27-bit hex to 32-bit hex
            matrix.append(binToFloat32(matrixConstant))

            # this line contains n conn
            if lineNumber == 52:
                nConn = regSlice(line, 29, 28)

            # these lines contain module IDs
            if lineNumber <= 50 and (lineNumber-1) % 10 != 0:
                moduleNumber = (lineNumber - 1) // 10
                IDIndex = (lineNumber - 1) % 10
                alteredID = globalModuleIDs[moduleNumber]
                setBit(alteredID, IDIndex*2-1, regSlice(line, 29, 29))
                setBit(alteredID, IDIndex*2-2, regSlice(line, 28, 28))
                globalModuleIDs[moduleNumber] = alteredID

    # cleaning up
    globalModuleIDs = [int(''.join(ID), 2) for ID in globalModuleIDs]
    sectorID = globalModuleIDs.pop(4)
    vectorIndexes = [1, 13, 25, 37, 49]
    for index in sorted(vectorIndexes, reverse=True):
        vector.append(matrix.pop(index-1))
    vector = list(reversed(vector))
    matrix = np.array(matrix).reshape(5, 11)

    # return sector ID, vector, and matrix
    return (sectorID_8L, vector, matrix, globalModuleIDs) # the other sectorID is for TF?

def extractConstants(extrapolatorConstants_Lines):

    sectorIDs = []
    vectors = []
    matrices = []
    globalModuleIDsList = []

    nLines = len(extrapolatorConstants_Lines)
    nMatrices = 0

    while (nMatrices+1)*64 <= nLines:
        sectorID, vector, matrix, globalModuleIDs = extractOneSetOfConstants(extrapolatorConstants_Lines[nMatrices*64:nMatrices*64+63])
        sectorIDs.append(sectorID)
        vectors.append(vector)
        matrices.append(matrix)
        globalModuleIDsList.append(globalModuleIDs)
        nMatrices += 1
 
    return dict(zip(sectorIDs, zip(vectors, matrices, globalModuleIDsList))) # dictionary where sector IDs are keys
