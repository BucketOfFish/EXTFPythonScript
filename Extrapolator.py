import numpy as np
from math import floor


def getExtrapolatedGlobalSSIDs(extrapolatorConstants, AUXTrackCoordinates, localModuleIDDictionary, tower):
    '''For every track, compute the extrapolated global SSIDs (expanded to one module on any side), and
    return a list of lists, such as [[track 1 extr.], [track 2 extr.]...]. For each track, the list is composed
    of (global SSID, layer), such as [(2412, 0), (2462, 0)... (2111, 7)...].'''

    # returned values
    globalSSIDs = []

    for hitCoordinateValues in AUXTrackCoordinates:

        sectorID = (hitCoordinateValues[0], 0)  # we're only considering connection 0 for now
        coordinates = np.array(hitCoordinateValues[1])

        if sectorID in extrapolatorConstants:  # if we have matrix, vector, etc. info stored for this sector ID

            vector = np.array(extrapolatorConstants[sectorID][0])  # vector and matrix data (60 constants)
            matrix = np.array(extrapolatorConstants[sectorID][1])
            globalModuleIDs = np.array(extrapolatorConstants[sectorID][2])  # global module IDs for SCT and IBL layer hits

            extrapolatedCoordinates = vector + matrix.dot(coordinates)  # perform matrix extrapolation - this gives [IBL_phi IBL_eta SCT SCT SCT]
            localSSIDCoordinates = extrapolatedCoordinates / 16.0  # SCT is scaled by 1/16
            # keep eta and phi coordinates of IBL separate for now - we need to see if they fall outside the module
            localSSIDCoordinates[0] = extrapolatedCoordinates[0] / 64.0  # IBL phi is scaled by 1/64
            localSSIDCoordinates[1] = extrapolatedCoordinates[1] / (16 * 16.32)  # IBL eta is scaled by a different constant
            localSSIDCoordinates = [int(floor(number)) for number in localSSIDCoordinates]  # next, floor - for e.g. -0.5, go to -1

            expandedLocalSSIDs = []  # look at the SSIDs surrounding each of our extrapolated SSIDs - grid of width 42 and height 10

            # add SSIDs surrounding the extrapolated IBL SSID
            IBLPhi = localSSIDCoordinates[0]
            IBLEta = localSSIDCoordinates[1]
            lowPhi = max(IBLPhi-1, 0)
            highPhi = min(IBLPhi+1, 41)
            lowEta = max(IBLEta-1, 0)
            highEta = min(IBLEta+1, 9)
            for i in range(lowEta, highEta+1):
                for j in range(lowPhi, highPhi+1):
                    expandedLocalSSIDs.append(i*42 + j)
            nSSIDsInGroup = [len(expandedLocalSSIDs)]

            # add SSIDs surrounding the extrapolated SCT SSIDs
            for SSID in (localSSIDCoordinates[2], localSSIDCoordinates[3], localSSIDCoordinates[4]):
                lowSSID = max(SSID-1, 0)
                highSSID = min(SSID+1, 95)
                for i in range(lowSSID, highSSID+1):
                    expandedLocalSSIDs.append(i)
                nSSIDsInGroup.append(highSSID+1-lowSSID)

            localModuleIDs = []

            def addLocalModuleID(key):
                if key in localModuleIDDictionary:
                    localModuleIDs.append(localModuleIDDictionary[key])
                else:
                    localModuleIDs.append(0)
                    print("WARNING:", key, "not in local/global module ID dictionary")
            addLocalModuleID((tower, 0, globalModuleIDs[0]))
            addLocalModuleID((tower, 5, globalModuleIDs[1]))
            addLocalModuleID((tower, 7, globalModuleIDs[2]))
            addLocalModuleID((tower, 11, globalModuleIDs[3]))

            newLayers = [0] * nSSIDsInGroup[0] + [5] * nSSIDsInGroup[1] + [7] * nSSIDsInGroup[2] + [11] * nSSIDsInGroup[3]  # local module IDs are not unique across layers, so we need to keep this info
            expandedLocalModuleIDs = [localModuleIDs[0]] * nSSIDsInGroup[0] + [localModuleIDs[1]] * nSSIDsInGroup[1] + [localModuleIDs[2]] * nSSIDsInGroup[2] + [localModuleIDs[3]] * nSSIDsInGroup[3]

            expandedGlobalSSIDs = np.array(expandedLocalModuleIDs) * 96 + np.array(expandedLocalSSIDs)  # SCT
            for i in range(nSSIDsInGroup[0]):
                expandedGlobalSSIDs[i] = expandedLocalModuleIDs[i] * 420 + expandedLocalSSIDs[i]  # IBL

            globalSSIDs.append(list(zip(list(expandedGlobalSSIDs), newLayers)))

            # print("Track in sector ID", sectorID, "has coordinates:", hitCoordinateValues[1])
            # print("\tGlobal module IDs after extrapolation:", globalModuleIDs)
            # print("\tConverted to local module IDs:", localModuleIDs)
            # print("\tTrack has extrapolated coordinates:", extrapolatedCoordinates)
            # print("\tThese coordinates are within local SSIDs:", localSSIDCoordinates)
            # print("\tIncluding neighboring local SSIDs:", expandedLocalSSIDs)
            # print("\tCorresponding to global SSIDs:", expandedGlobalSSIDs)

        else:
            print("Sector ID", sectorID, "is not in matrix data.")
            globalSSIDs.append([])

    print("")
    return globalSSIDs
