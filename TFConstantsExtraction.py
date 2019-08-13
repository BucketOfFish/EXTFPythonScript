import numpy as np
import Utilities as U


def extractOneSetOfConstants(constants_Lines):
    '''For each sector ID, we have 384 lines of length 32 bits each, and these 384 lines are split into 6 blocks
    (with block transfer numbers from 0-5). This function extracts data and returns in a dictionary with sector IDs
    as keys, and values as (S matrix, h vector, c mat., q vec., inverted C mat.). The inverted C matrices are
    [[matrix for missing layer 0], [ML1]...].'''

    # extracted values
    sectorID = []  # I think this function should only get one sector ID actually, but I coded this really fast
    SMatrix = []  # chi2 calculation matrix
    hVector = []  # chi2 additive vector
    cMatrix = []  # calculation matrix for (d0, z0, cot[theta], phi0, curv)
    qVector = []  # additive vector for (d0, z0, cot[theta], phi0, curv)
    invCMatrices = [np.zeros((2, 2)), np.zeros((2, 2)), np.zeros((2, 2)), np.zeros((2, 2)), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1), np.zeros(1)]  # inverse C matrices

    # extract one block (cooresponding to a block transfer number) at a time
    blockN = 0
    placeholderVector = []  # for use in filling matrices, one line at a time

    while blockN < 6:

        blockLines = constants_Lines[blockN*64:blockN*64+63]  # read one block at a time

        # read through each line of the block
        for lineNumber, line in enumerate(blockLines, start=1):

            # first line is sector ID and block transfer number
            if lineNumber == 1:
                sectorID = int(U.regSlice(line, 19, 4), 2)
                # blockTransferN = int(regSlice(line, 3, 0), 2)  # CHECKPOINT

            else:
                constant = U.binToFloat32(line[5:] + "00000")  # strip off the first bits and put them at the end - just dumb formatting for changing from 27-bit hex to 32-bit hex

                subBlock = (lineNumber-3) / 20  # each block has three subblocks (except for the last block, which only has one)
                subLineNumber = (lineNumber-3) % 20  # to tell which line we're on in the subblock

                if subBlock >= 3:
                    continue  # these are blank lines
                if blockN == 5 and subBlock >= 1:
                    continue  # these too

                ############################################
                # oh boy, fill those matrices and vectors! #
                ############################################

                # inverse C constants depend on block number - when only one constant is needed, the first line is blank:
                # 0 - missing layer 0 C11, C12 - ML0 C21, C22 - ML1 C11 C12
                # 1 - ML1 C21, C22 - ML2 C11, C12 - ML2 C21 C22
                # 2 - ML3 C11, C12 - ML3 C21, C22 - ML4
                # 3 - ML5 - ML6 - ML7
                # 4 - ML8 - ML9 - ML10
                # 5 - ML11

                if subLineNumber == 0:  # inverse C constants
                    if blockN == 0:
                        if subBlock == 0:
                            invCMatrices[0][0, 0] = constant
                        elif subBlock == 1:
                            invCMatrices[0][1, 0] = constant
                        elif subBlock == 2:
                            invCMatrices[1][0, 0] = constant
                    elif blockN == 1:
                        if subBlock == 0:
                            invCMatrices[1][1, 0] = constant
                        elif subBlock == 1:
                            invCMatrices[2][0, 0] = constant
                        elif subBlock == 2:
                            invCMatrices[2][1, 0] = constant
                    elif blockN == 2:
                        if subBlock == 0:
                            invCMatrices[3][0, 0] = constant
                        elif subBlock == 1:
                            invCMatrices[3][1, 0] = constant

                elif subLineNumber == 1:  # inverse C constants
                    if blockN == 0:
                        if subBlock == 0:
                            invCMatrices[0][0, 1] = constant
                        elif subBlock == 1:
                            invCMatrices[0][1, 1] = constant
                        elif subBlock == 2:
                            invCMatrices[1][0, 1] = constant
                    elif blockN == 1:
                        if subBlock == 0:
                            invCMatrices[1][1, 1] = constant
                        elif subBlock == 1:
                            invCMatrices[2][0, 1] = constant
                        elif subBlock == 2:
                            invCMatrices[2][1, 1] = constant
                    elif blockN == 2:
                        if subBlock == 0:
                            invCMatrices[3][0, 1] = constant
                        elif subBlock == 1:
                            invCMatrices[3][1, 1] = constant
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

                elif subLineNumber == 2:  # vector constant
                    if blockN >= 0 and blockN <= 3 and not (blockN == 3 and subBlock == 2):  # chi^2 vector
                        hVector.append(constant)
                    else:  # track parameters vector (d0, z0, cot[theta], phi0, curv)
                        qVector.append(constant)

                elif subLineNumber >= 3 and subLineNumber <= 18:  # matrix constants
                    if subLineNumber == 3:
                        placeholderVector = [constant]
                    else:
                        placeholderVector.insert(0, constant)
                    if subLineNumber == 18:
                        if blockN >= 0 and blockN <= 3 and not (blockN == 3 and subBlock == 2):  # chi^2 matrix
                            SMatrix.append(placeholderVector)
                        else:  # track parameters matrix (d0, z0, cot[theta], phi0, curv)
                            cMatrix.append(placeholderVector)

                ############################################
                # oh boy, fill those matrices and vectors! #
                ############################################

        blockN += 1

    # return constants
    return (sectorID, np.array(SMatrix), np.array(hVector), np.array(cMatrix), np.array(qVector), invCMatrices)


def extractConstants(constants_Lines):

    sectorIDs = []; SMatrices = []; hVectors = []; cMatrices = []; qVectors = []; allInvCMatrices = []  # NOQA

    nLines = len(constants_Lines)
    nSectors = 0
    sectorSize = 384

    # every 384 lines of TF constants file contains info for one sector ID
    while (nSectors+1)*sectorSize <= nLines:
        sectorID, SMatrix, hVector, cMatrix, qVector, invCMatrices = extractOneSetOfConstants(constants_Lines[nSectors*sectorSize:(nSectors+1)*sectorSize-1])
        sectorIDs.append(sectorID)
        SMatrices.append(SMatrix)
        hVectors.append(hVector)
        cMatrices.append(cMatrix)
        qVectors.append(qVector)
        allInvCMatrices.append(invCMatrices)
        nSectors += 1

    return dict(zip(sectorIDs, zip(SMatrices, hVectors, cMatrices, qVectors, allInvCMatrices)))  # dictionary where sector IDs are keys
