import numpy as np
from Utilities import *

# given 64 lines of 32 bits each, this function extracts a vector, a matrix, and other info such as module IDs
def extractMatrix(matrixConstantsFileLines):

    # extracted values
    matrix = []
    vector = []
    emptyID = list('000000000000000000') # some stupid Python nonsense
    moduleIDs = [list(emptyID), list(emptyID), list(emptyID), list(emptyID), list(emptyID)]
    sectorID = list(emptyID) # the fifth element of moduleIDs is the sector ID - will be separated at the end
    sectorID_8L = []
    connID = []
    nConn = []

    # read through each line of the file
    for lineNumber, line in enumerate(matrixConstantsFileLines, start=1):

        # first line is 8L sector ID and conn ID
        if lineNumber == 1:
            sectorID_8L = regSlice(line, 29, 2)
            connID = regSlice(line, 1, 0)

        elif lineNumber <= 61:
            # these lines contain constants
            matrix.append(regSlice(line, 26, 0))

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
    moduleIDs = [''.join(ID) for ID in moduleIDs]
    sectorID = moduleIDs.pop(4)
    vectorIndexes = [1, 13, 25, 37, 49]
    for index in sorted(vectorIndexes, reverse=True):
        vector.append(matrix.pop(index-1))
    vector = list(reversed(vector))
    matrix = np.array(matrix).reshape(5, 11)
