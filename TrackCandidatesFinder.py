from collections import defaultdict

# return all combinations of hit candidates for track fitting
# return in the form [([track candidates for 8L input], track sector ID), ([track candidates], sector ID)...], where [track candidates] = [[16 hit coords], [16 hit coords]...], and layer 0 is the first hit coords
def listTrackCandidates(AUXHits, AUXExtrapolatedGlobalSSIDs, DFGlobalSSIDs):

    # DFGlobalSSIDs contains SSID, layer, and coordinate info - we take just the first two for matching purposes
    DFSSIDsToMatch = [info[0:2] for info in DFGlobalSSIDs]

    # find all candidate DF hits
    DFCoordinates = []
    for trackExtrapolatedSSIDs in AUXExtrapolatedGlobalSSIDs:
        matchedCoordinates = []
        for SSID in trackExtrapolatedSSIDs:
        # check if extrapolated hits are among DF hits
            for index, DFSSID in enumerate(DFSSIDsToMatch):
                if SSID == DFSSID:
                    matchedDFInfo = DFGlobalSSIDs[index]
                    matchedCoordinates.append((matchedDFInfo[2], matchedDFInfo[1])) # convert DF SSIDs back into coordinates
        DFCoordinates.append(matchedCoordinates)

    # combine the 12-layer hit coordinates with layer info
    twelveLayerHits = []
    sectorIDs = [coord[0] for coord in AUXHits] # sector ID of track
    AUXCoordinates = [coord[1] for coord in AUXHits] # coordinates of original 8-layer hit
    AUXCoordinates = [[([coord[0], coord[1]], 1), ([coord[2], coord[3]], 2), ([coord[4], coord[5]], 3), (coord[6], 4), (coord[7], 6), (coord[8], 8), (coord[9], 9), (coord[10], 10)] for coord in AUXCoordinates] # organize by layer - for IBL, do row, col
    allCoordinatesInfo = [coord + exCoord for coord, exCoord in zip(AUXCoordinates, DFCoordinates)] # coordinates for all 12 layers
    allCoordinatesInfo = [sorted(coordinates, key = lambda coord: coord[1]) for coordinates in allCoordinatesInfo] # sort coordinate info by layer number

    # organization of coordinate info, to make it easier to feed to the track fitter
    allSortedCoordinates = []
    for coordinatesInfo in allCoordinatesInfo:
        sortedCoordinates = defaultdict(list)
        for coordinates, layer in coordinatesInfo:
            sortedCoordinates[layer].append(coordinates)
        allSortedCoordinates.append(sortedCoordinates)

    # add in -1 placeholders for layers that don't have hit info
    for sortedCoordinates in allSortedCoordinates:
        for layer in range(12):
            if layer not in sortedCoordinates.keys():
                if layer <= 3: # IBL layer
                    sortedCoordinates[layer] = [[-1, -1]]
                else:
                    sortedCoordinates[layer] = [-1]

    # make lists of all candidates hits for each track
    trackCandidates = []
    for trackInfo in allSortedCoordinates:
        possibleTracks = [[]]
        for layer in range(12):
            currentPossibleTracks = list(possibleTracks) # deep copy of list
            possibleTracks = []
            for possibleHit in trackInfo[layer]:
                if type(possibleHit) is not list: possibleHit = [possibleHit]
                newPossibilities = [track + possibleHit for track in currentPossibleTracks]
                possibleTracks += newPossibilities
        trackCandidates.append(possibleTracks)

    return zip(trackCandidates, sectorIDs)
