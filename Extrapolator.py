import numpy as np
from math import floor

# for every track, compute the extrapolated global SSIDs (expanded to one module on any side)
# returns a list of lists, such as [[track 1 extr.], [track 2 extr.]...]
# for each track, the list is composed of (global SSID, layer), such as [(2412, 0), (2462, 0)... (2111, 7)...]
def getExtrapolatedGlobalSSIDs(matrixValues, hitCoordinates, localModuleIDDictionary, tower):

    # returned values
    globalSSIDs = []

    for hitCoordinateValues in hitCoordinates:

        sectorID = (hitCoordinateValues[0], 0) # we're only considering connection 0 for now
        coordinates = np.array(hitCoordinateValues[1])

        if sectorID in matrixValues: # if we have matrix, vector, etc. info stored for this sector ID

            vector = np.array(matrixValues[sectorID][0]) # vector and matrix data (60 constants)
            matrix = np.array(matrixValues[sectorID][1])
            globalModuleIDs = np.array(matrixValues[sectorID][2]) # global module IDs for SCT and IBL layer hits

            extrapolatedCoordinates = vector + matrix.dot(coordinates) # perform matrix extrapolation - this gives [IBL_phi IBL_eta SCT SCT SCT]
            localSSIDCoordinates = extrapolatedCoordinates / 16.0 # SCT is scaled by 1/16
            # keep eta and phi coordinates of IBL separate for now - we need to see if they fall outside the module
            localSSIDCoordinates[0] = extrapolatedCoordinates[0] / 64.0 # IBL phi is scaled by 1/64
            localSSIDCoordinates[1] = extrapolatedCoordinates[1] / (16 * 16.32) # IBL eta is scaled by a different constant
            localSSIDCoordinates = [int(floor(number)) for number in localSSIDCoordinates] # next, floor - for e.g. -0.5, go to -1

            expandedLocalSSIDs = [] # look at the SSIDs surrounding each of our extrapolated SSIDs - grid of width 42 and height 10

            ################################
            # WARNING: Stupid code follows #
            ################################

            # add SSIDs surrounding the extrapolated IBL SSID
            IBLPhi = localSSIDCoordinates[0]
            IBLEta = localSSIDCoordinates[1]
            if IBLPhi < -1 or IBLPhi > 42 or IBLEta < -1 or IBLEta > 10: # outside of module by more than one row
                pass
            elif IBLPhi == -1 or IBLPhi == 42 or IBLEta == -1 or IBLEta == 10: # outside of module by one row
                bottomRow = (IBLEta == -1)
                topRow = (IBLEta == 10)
                leftRow = (IBLPhi == -1)
                rightRow = (IBLPhi == 42)
                if bottomRow and leftRow:
                    expandedLocalSSIDs.append(IBLPhi+1 + ((IBLEta+1) * 42))
                elif bottomRow and rightRow:
                    expandedLocalSSIDs.append(IBLPhi-1 + ((IBLEta+1) * 42))
                elif topRow and leftRow:
                    expandedLocalSSIDs.append(IBLPhi+1 + ((IBLEta-1) * 42))
                elif topRow and rightRow:
                    expandedLocalSSIDs.append(IBLPhi-1 + ((IBLEta-1) * 42))
                elif bottomRow:
                    expandedLocalSSIDs.append(IBLPhi-1 + ((IBLEta+1) * 42))
                    expandedLocalSSIDs.append(IBLPhi + ((IBLEta+1) * 42))
                    expandedLocalSSIDs.append(IBLPhi+1 + ((IBLEta+1) * 42))
                elif topRow:
                    expandedLocalSSIDs.append(IBLPhi-1 + ((IBLEta-1) * 42))
                    expandedLocalSSIDs.append(IBLPhi + ((IBLEta-1) * 42))
                    expandedLocalSSIDs.append(IBLPhi+1 + ((IBLEta-1) * 42))
                elif leftRow:
                    expandedLocalSSIDs.append(IBLPhi+1 + ((IBLEta-1) * 42))
                    expandedLocalSSIDs.append(IBLPhi+1 + (IBLEta * 42))
                    expandedLocalSSIDs.append(IBLPhi+1 + ((IBLEta+1) * 42))
                elif rightRow:
                    expandedLocalSSIDs.append(IBLPhi-1 + ((IBLEta-1) * 42))
                    expandedLocalSSIDs.append(IBLPhi-1 + (IBLEta * 42))
                    expandedLocalSSIDs.append(IBLPhi-1 + ((IBLEta+1) * 42))
            else: # inside module
                bottomRow = (IBLEta == 0)
                topRow = (IBLEta == 9)
                leftRow = (IBLPhi == 0)
                rightRow = (IBLPhi == 41)
                IBLLocalSSID = IBLPhi + (IBLEta * 42) # IBL local SSID is eta times 42, plus phi
                expandedLocalSSIDs.append(IBLLocalSSID)
                if bottomRow and leftRow:
                    expandedLocalSSIDs.append(IBLLocalSSID + 1)
                    expandedLocalSSIDs.append(IBLLocalSSID + 42)
                    expandedLocalSSIDs.append(IBLLocalSSID + 43)
                elif bottomRow and rightRow:
                    expandedLocalSSIDs.append(IBLLocalSSID - 1)
                    expandedLocalSSIDs.append(IBLLocalSSID + 41)
                    expandedLocalSSIDs.append(IBLLocalSSID + 42)
                elif topRow and leftRow:
                    expandedLocalSSIDs.append(IBLLocalSSID + 1)
                    expandedLocalSSIDs.append(IBLLocalSSID - 41)
                    expandedLocalSSIDs.append(IBLLocalSSID - 42)
                elif topRow and rightRow:
                    expandedLocalSSIDs.append(IBLLocalSSID - 1)
                    expandedLocalSSIDs.append(IBLLocalSSID - 42)
                    expandedLocalSSIDs.append(IBLLocalSSID - 43)
                elif bottomRow:
                    expandedLocalSSIDs.append(IBLLocalSSID - 1)
                    expandedLocalSSIDs.append(IBLLocalSSID + 1)
                    expandedLocalSSIDs.append(IBLLocalSSID + 41)
                    expandedLocalSSIDs.append(IBLLocalSSID + 42)
                    expandedLocalSSIDs.append(IBLLocalSSID + 43)
                elif topRow:
                    expandedLocalSSIDs.append(IBLLocalSSID - 1)
                    expandedLocalSSIDs.append(IBLLocalSSID + 1)
                    expandedLocalSSIDs.append(IBLLocalSSID - 41)
                    expandedLocalSSIDs.append(IBLLocalSSID - 42)
                    expandedLocalSSIDs.append(IBLLocalSSID - 43)
                elif leftRow:
                    expandedLocalSSIDs.append(IBLLocalSSID + 1)
                    expandedLocalSSIDs.append(IBLLocalSSID + 42)
                    expandedLocalSSIDs.append(IBLLocalSSID + 43)
                    expandedLocalSSIDs.append(IBLLocalSSID - 41)
                    expandedLocalSSIDs.append(IBLLocalSSID - 42)
                elif rightRow:
                    expandedLocalSSIDs.append(IBLLocalSSID - 1)
                    expandedLocalSSIDs.append(IBLLocalSSID + 41)
                    expandedLocalSSIDs.append(IBLLocalSSID + 42)
                    expandedLocalSSIDs.append(IBLLocalSSID - 42)
                    expandedLocalSSIDs.append(IBLLocalSSID - 43)
                else:
                    expandedLocalSSIDs.append(IBLLocalSSID + 41)
                    expandedLocalSSIDs.append(IBLLocalSSID + 42)
                    expandedLocalSSIDs.append(IBLLocalSSID + 43)
                    expandedLocalSSIDs.append(IBLLocalSSID - 1)
                    expandedLocalSSIDs.append(IBLLocalSSID + 1)
                    expandedLocalSSIDs.append(IBLLocalSSID - 41)
                    expandedLocalSSIDs.append(IBLLocalSSID - 42)
                    expandedLocalSSIDs.append(IBLLocalSSID - 43)
            nSSIDsInGroup = [len(expandedLocalSSIDs)]

            # add SSIDs surrounding the extrapolated SCT SSIDs
            for SSID in (localSSIDCoordinates[2], localSSIDCoordinates[3], localSSIDCoordinates[4]):
                if SSID < -1 or SSID > 96: # 96 SCT modules in tower
                    pass
                    nSSIDsInGroup.append(0)
                elif SSID == -1:
                    expandedLocalSSIDs.append(0)
                    nSSIDsInGroup.append(1)
                elif SSID == 96:
                    expandedLocalSSIDs.append(95)
                    nSSIDsInGroup.append(1)
                elif SSID == 0:
                    expandedLocalSSIDs.append(0)
                    expandedLocalSSIDs.append(1)
                    nSSIDsInGroup.append(2)
                elif SSID == 95:
                    expandedLocalSSIDs.append(94)
                    expandedLocalSSIDs.append(95)
                    nSSIDsInGroup.append(2)
                else:
                    expandedLocalSSIDs.append(SSID - 1)
                    expandedLocalSSIDs.append(SSID)
                    expandedLocalSSIDs.append(SSID + 1)
                    nSSIDsInGroup.append(3)

            ###################
            # End stupid code #
            ###################

            localModuleIDs = []
            def addLocalModuleID(key):
                if key in localModuleIDDictionary:
                    localModuleIDs.append(localModuleIDDictionary[key])
                else:
                    localModuleIDs.append(0)
                    print "WARNING:", key, "not in local/global module ID dictionary"
            addLocalModuleID((tower, 0, globalModuleIDs[0]))
            addLocalModuleID((tower, 5, globalModuleIDs[1]))
            addLocalModuleID((tower, 7, globalModuleIDs[2]))
            addLocalModuleID((tower, 11, globalModuleIDs[3]))

            newLayers = [0] * nSSIDsInGroup[0] + [5] * nSSIDsInGroup[1] + [7] * nSSIDsInGroup[2] + [11] * nSSIDsInGroup[3] # local module IDs are not unique across layers, so we need to keep this info
            localModuleIDs = [localModuleIDs[0]] * nSSIDsInGroup[0] + [localModuleIDs[1]] * nSSIDsInGroup[1] + [localModuleIDs[2]] * nSSIDsInGroup[2] + [localModuleIDs[3]] * nSSIDsInGroup[3]

            expandedGlobalSSIDs = np.array(localModuleIDs) * 96 + np.array(expandedLocalSSIDs) # SCT
            for i in range(nSSIDsInGroup[0]):
                expandedGlobalSSIDs[i] = localModuleIDs[i]  * 420 + expandedLocalSSIDs[i] # IBL

            globalSSIDs.append(zip(list(expandedGlobalSSIDs), newLayers))

            # print "Track in sector ID", sectorID, "has extrapolated coordinates:", extrapolatedCoordinates
            # print "Track in sector ID", sectorID, "has extrapolated local SSIDs:", expandedLocalSSIDs
            # print "Track in sector ID", sectorID, "has global module IDs:", globalModuleIDs
            # print "Track in sector ID", sectorID, "has local module IDs:", localModuleIDs
            # print "Track in sector ID", sectorID, "has expanded global SSIDs: ", " ".join([hex(i) for i in expandedGlobalSSIDs])
            # print "Track in sector ID", sectorID, "has expanded global SSIDs:", expandedGlobalSSIDs

        else:
            print "Sector ID", sectorID, "is not in matrix data."
            globalSSIDs.append([])

    return globalSSIDs
