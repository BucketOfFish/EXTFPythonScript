from collections import defaultdict

# return all combinations of hit candidates for track fitting
def listTrackCandidates(AUXHits, AUXExtrapolatedGlobalSSIDs, DFGlobalSSIDs):

    # find all sets of candidate 12-layer hits
    matchedDFExtrapolatedSSIDs = []
    for trackExtrapolatedSSIDs in AUXExtrapolatedGlobalSSIDs:
        trackMatchedExtrapolatedSSIDs = []
        for SSID in trackExtrapolatedSSIDs:
        # check if extrapolated hits are among DF hits
            if SSID in DFGlobalSSIDs:
                trackMatchedExtrapolatedSSIDs.append(SSID)
                # print "Extrapolated hit at (global SSID, layer)", SSID, "found in DF hits."
            # else:
                # print "Extrapolated hit at (global SSID, layer)", SSID, "not found."
        matchedDFExtrapolatedSSIDs.append(trackMatchedExtrapolatedSSIDs)

    # combine the 12-layer hit coordinates with layer info
    twelveLayerHits = []
    AUXCoordinates = [coord[1] for coord in AUXHits] # coordinates of original 8-layer hit
    AUXCoordinates = [[((coord[0], coord[1]), 1), ((coord[2], coord[3]), 2), ((coord[4], coord[5]), 3), (coord[6], 4), (coord[7], 6), (coord[8], 8), (coord[9], 9), (coord[10], 10)] for coord in AUXCoordinates] # organize by layer
    # AUXExtrapolatedCoordinates = AUXExtrapolatedGlobalSSIDs # CHECKPOINT - haven't actually transformed SSIDs into coordinates yet
    AUXExtrapolatedCoordinates = matchedDFExtrapolatedSSIDs # CHECKPOINT - haven't actually transformed SSIDs into coordinates yet
    allCoordinatesInfo = [coord + exCoord for coord, exCoord in zip(AUXCoordinates, AUXExtrapolatedCoordinates)] # coordinates for all 12 layers
    allCoordinatesInfo = [sorted(coordinates, key = lambda coord: coord[1]) for coordinates in allCoordinatesInfo] # sort coordinate info by layer number

    # organization of coordinate info, to make it easier to feed to the track fitter
    allSortedCoordinates = []
    for coordinatesInfo in allCoordinatesInfo:
        sortedCoordinates = defaultdict(list)
        for coordinates, layer in coordinatesInfo:
            sortedCoordinates[layer].append(coordinates)
        allSortedCoordinates.append(sortedCoordinates)

    trackCandidates = allSortedCoordinates
    return trackCandidates
