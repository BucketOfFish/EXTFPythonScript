from math import floor

# get glocal SSIDs for DF hits
# return list of (global SSID, layer, coordinates) for hits
def getDFGlobalSSIDs(DFCoordinates, localModuleIDDictionary, tower):

    globalSSIDs = []
    layers = []
    allCoordinates = []

    for hitCoordinateValues in DFCoordinates:

        globalModuleID = hitCoordinateValues[0]
        coordinates = hitCoordinateValues[1]
        isIBLHit = (len(coordinates) == 2) # are these IBL or SCT coordinates

        localSSIDCoordinates = []
        localModuleID = -1
        layer = -1
        localSSID = -1

        if isIBLHit:
            localSSIDCoordinates.append(coordinates[0] / 64.0) # IBL phi is scaled by 1/64
            localSSIDCoordinates.append(coordinates[1] / (16 * 16.32)) # IBL eta is scaled by a different constant
        else:
            localSSIDCoordinates = [coordinates[0] / 16.0] # first step of local SSID mapping is scaling the extrapolated parameters
        localSSIDCoordinates = [int(floor(number)) for number in localSSIDCoordinates] # next, floor - for e.g. -0.5, go to -1
        # print("Local SSID Coordinates:", localSSIDCoordinates)

        if isIBLHit:
            if (tower, 0, globalModuleID) in localModuleIDDictionary:
                localModuleID = localModuleIDDictionary[(tower, 0, globalModuleID)] # use dictionary to find the local module ID
            layer = 0
            IBLPhi = localSSIDCoordinates[0]
            IBLEta = localSSIDCoordinates[1]
            localSSID = IBLPhi + (IBLEta * 42)
        else:
            SCTLayers = [5, 7, 11] # don't know which layer this module ID is on, so check which one exists in the module map
            for SCTLayer in SCTLayers: # check dictionary for all three SCT layers - global module ID is only on one of them
                if (tower, SCTLayer, globalModuleID) in localModuleIDDictionary:
                    localModuleID = localModuleIDDictionary[(tower, SCTLayer, globalModuleID)]
                    layer = SCTLayer
            localSSID = localSSIDCoordinates[0]

        if localModuleID == -1:
            # print("Global module ID", globalModuleID, "not found in dictionary")
            continue
        # print("Local module ID and SSID:", localModuleID, localSSID)

        if isIBLHit:
            globalSSID = localModuleID * 420 + localSSID # IBL
        else:
            globalSSID = localModuleID * 96 + localSSID # SCT

        if sum(coordinates) != 0: # temp fix - we're getting spurious (0, 0) hits in our input data
            globalSSIDs.append(globalSSID)
            layers.append(layer)
            allCoordinates.append(coordinates)
            # print("Global SSID:", globalSSID)

    return list(zip(globalSSIDs, layers, allCoordinates)) # global SSID is apparently not unique across different SCT layers
