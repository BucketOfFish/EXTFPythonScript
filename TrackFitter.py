import numpy as np

# calculate TF stuff using paper "Linear Fit within Missing-Hit Roads in FTKSim" by Annovi et al.
def fitTracks(trackCandidates):

    # x, c, q, S, h, C, t defined as in the paper - with TF_ prefix because I don't like single-character variable names
    S = np.random.rand(16,16) # CHECKPOINT - S is not actually a random matrix
    h = np.random.rand(1,16) # CHECKPOINT - h is not actually a random vector

    for sortedCoordinates in trackCandidates:

        nHits = len(sortedCoordinates)
        availableLayers = sortedCoordinates.keys()
        # loop over all combinations of possible coordinates (one choice for each layer)
        coordinates = []
        for layer in range(12):
            if layer in availableLayers: # CHECKPOINT - only using one combination now
                currentCoordinate = sortedCoordinates[layer][0]
                if (isinstance(currentCoordinate, int)):
                    coordinates.append(currentCoordinate)
                else:
                    coordinates.append(currentCoordinate[0])
                    coordinates.append(currentCoordinate[1])
            else:
                if layer <= 3:
                    coordinates.append(-1) # use -1 to indicate layer with non-existent hit info
                    coordinates.append(-1)
                else:
                    coordinates.append(-1)
        if nHits < 8: # CHECKPOINT - not enough hits, but check if 8
            continue
        else:
            print coordinates
            # TF_x
            # TFMatrixValues
            # if len(TF_x) < fullLength: # estimate missing coordinates in order to minimize fit quality estimator
                # TF_C = blah blah TF_S
                # TF_t = blah
                # TF_x = TF_x + missingCoordinates
            # trackParameters = TF_c * TF_x + TF_q
            # fitQualityEstimator = vectorLength(TF_S * TF_x + TF_h)
