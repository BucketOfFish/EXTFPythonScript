import numpy as np
from Utilities import *

# given 384 lines of 32 bits each, this function extracts all the track fitter constants (as well as inverse C matrices)
# the return form is a dictionary with sector IDs as keys, and values as (S matrix, h vector, c matrix, q vector, inverted C matrices)
# the inverted C matrices are [[matrix for missing layer 0], [ML1]...]
def extractOneSetOfConstants(constants_Lines):

    # extracted values - some dumb coding here, but I just want to get this done
    sectorID = []
    SMatrix = []
    hVector = []
    cMatrix = []
    qVector = []
    invCMatrices = [np.zeros((2,2)), np.zeros((2,2)), np.zeros((2,2)), np.zeros((2,2)), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1)]

    # extract one block at a time
    nLines = len(constants_Lines)
    blockN = 0
    placeholderVector = [] # for use in filling matrices, one constant at a time

    while blockN < 6:

        blockLines = constants_Lines[blockN*64:blockN*64+63]

        # read through each line of the block
        for lineNumber, line in enumerate(blockLines, start=1):

            # first line is sector ID and block transfer number
            if lineNumber == 1:
                sectorID = int(regSlice(line, 19, 4), 2)
                # blockNCheck = int(regSlice(line, 3, 0), 2)
                # print blockN == blockNCheck

            else:
                constant = binToFloat32(line)
                subBlock = (lineNumber-3) / 20
                subLineNumber = (lineNumber-3) % 20

                if blockN == 5 and subBlock >= 1: continue

                # inverse C constants depend on block number - when only one constant is needed, the first line is blank:
                # 0 - missing layer 0 C11, C12 - ML0 C21, C22 - ML1 C11 C12
                # 1 - ML1 C21, C22 - ML2 C11, C12 - ML2 C21 C22
                # 2 - ML3 C11, C12 - ML3 C21, C22 - ML4
                # 3 - ML5 - ML6 - ML7
                # 4 - ML8 - ML9 - ML10
                # 5 - ML11
                if subLineNumber == 0: # inverse C constants
                    if blockN == 0:
                        if subBlock == 0:
                            invCMatrices[0][0,0] = constant
                        elif subBlock == 1:
                            invCMatrices[0][1,0] = constant
                        elif subBlock == 2:
                            invCMatrices[1][0,0] = constant
                    elif blockN == 1:
                        if subBlock == 0:
                            invCMatrices[1][1,0] = constant
                        elif subBlock == 1:
                            invCMatrices[2][0,0] = constant
                        elif subBlock == 2:
                            invCMatrices[2][1,0] = constant
                    elif blockN == 2:
                        if subBlock == 0:
                            invCMatrices[3][0,0] = constant
                        elif subBlock == 1:
                            invCMatrices[3][1,0] = constant
                elif subLineNumber == 1: # inverse C constants
                    if blockN == 0:
                        if subBlock == 0:
                            invCMatrices[0][0,1] = constant
                        elif subBlock == 1:
                            invCMatrices[0][1,1] = constant
                        elif subBlock == 2:
                            invCMatrices[1][0,1] = constant
                    elif blockN == 1:
                        if subBlock == 0:
                            invCMatrices[1][1,1] = constant
                        elif subBlock == 1:
                            invCMatrices[2][0,1] = constant
                        elif subBlock == 2:
                            invCMatrices[2][1,1] = constant
                    elif blockN == 2:
                        if subBlock == 0:
                            invCMatrices[3][0,1] = constant
                        elif subBlock == 1:
                            invCMatrices[3][1,1] = constant
                        elif subBlock == 2:
                            invCMatrices[4][0] = constant
                    elif blockN == 3:
                        if subBlock == 0:
                            invCMatrices[5][0] = constant
                        elif subBlock == 1:
                            invCMatrices[6][0] = constant
                        elif subBlock == 2:
                            invCMatrices[7][0] = constant
                    elif blockN == 4:
                        if subBlock == 0:
                            invCMatrices[8][0] = constant
                        elif subBlock == 1:
                            invCMatrices[9][0] = constant
                        elif subBlock == 2:
                            invCMatrices[10][0] = constant
                    elif blockN == 5:
                        if subBlock == 0:
                            invCMatrices[11][0] = constant
                    
                elif subLineNumber == 2: # vector constant
                    if blockN >=0 and blockN <= 3 and not (blockN == 3 and subBlock == 2): # chi^2 vector
                        hVector.append(constant)
                    else: # track parameters vector (d0, z0, cot[theta], phi0, curv)
                        qVector.append(constant)

                elif subLineNumber >= 3 and subLineNumber <= 18: # matrix constants
                    if subLineNumber == 3 : placeholderVector = [constant]
                    else: placeholderVector.insert(0, constant)
                    if blockN >=0 and blockN <= 3 and not (blockN == 3 and subBlock == 2): # chi^2 vector
                        SMatrix.append(placeholderVector)
                    else: # track parameters vector (d0, z0, cot[theta], phi0, curv)
                        cMatrix.append(placeholderVector)

        blockN += 1

    # return constants
    return (sectorID, SMatrix, hVector, cMatrix, qVector, invCMatrices)

def extractConstants(constants_Lines):

    sectorIDs = []
    SMatrices = []
    hVectors = []
    cMatrices = []
    qVectors = []
    allInvCMatrices = []

    nLines = len(constants_Lines)
    nSectors = 0
    sectorSize = 384

    while (nSectors+1)*sectorSize <= nLines:
        sectorID, SMatrix, hVector, cMatrix, qVector, invCMatrices = extractOneSetOfConstants(constants_Lines[nSectors*sectorSize:(nSectors+1)*sectorSize-1])
        sectorIDs.append(sectorID)
        SMatrices.append(SMatrix)
        hVectors.append(hVector)
        cMatrices.append(cMatrix)
        qVectors.append(qVector)
        allInvCMatrices.append(invCMatrices)
        nSectors += 1
 
    return dict(zip(sectorIDs, zip(SMatrices, hVectors, cMatrices, qVectors, allInvCMatrices))) # dictionary where sector IDs are keys
