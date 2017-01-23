import numpy as np

# calculate TF stuff using paper "Linear Fit within Missing-Hit Roads in FTKSim" by Annovi et al.
# return in form of [[best track], [best track]...], where [best track] = [] if there are too few layers
def fitTracks(trackCandidates, TFConstants):

    bestTracks = []
    lostSectorIDs = []

    for trackInfo in trackCandidates:

        candidateSet = trackInfo[0]
        sectorID = trackInfo[1]

        print "Fitting track candidates in sector", sectorID # CHECKPOINT

        if sectorID not in TFConstants.keys():
            print "Track fitter constants not found for sector ID - fit terminated", sectorID
            lostSectorIDs.append(sectorID)
            # bestTracks.append([])
            continue

        # x, c, q, S, h, C, t defined as in the paper - with TF_ prefix because I don't like single-character variable names
        TF_S = TFConstants[sectorID][0]
        TF_h = TFConstants[sectorID][1]
        TF_c = TFConstants[sectorID][2]
        TF_q = TFConstants[sectorID][3]

        nCandidates = len(candidateSet)
        missingIndices = np.where(np.array(candidateSet[0]) == -1)[0]
        measuredIndices = np.where(np.array(candidateSet[0]) != -1)[0]
        nMissingIndices = len(missingIndices)
        nIBLLayers = sum(coord != -1 for coord in candidateSet[0][:8]) / 2 # IBL layers we have hits for
        nSCTLayers = sum(coord != -1 for coord in candidateSet[0][8:]) # SCT layers we have hits for
        nLayers = nIBLLayers + nSCTLayers

        bestTrackParameters = []
        bestFitQualityEstimator = -1

        if nLayers < 11: # not enough layers
            print "Not enough layers - fit terminated" # CHECKPOINT
            continue
        else:
            print "Fitting..." # CHECKPOINT
            for trackCandidate in candidateSet:
                TF_x = np.array(trackCandidate)
                if nLayers < 12: # missing layers
                    missingTF_S = TF_S[:, missingIndices]
                    measuredTF_S = TF_S[:, measuredIndices]
                    measuredTF_x = TF_x[measuredIndices]
                    TF_C = missingTF_S.transpose().dot(missingTF_S)
                    TF_t = - missingTF_S.transpose().dot(TF_h).transpose() - missingTF_S.transpose().dot(measuredTF_S.dot(measuredTF_x))
                    missingTF_x = np.linalg.inv(TF_C).dot(TF_t.transpose())
                    for index, xVal in enumerate(missingTF_x):
                        if isinstance(xVal, list):
                            TF_x[missingIndices[index]] = xVal[0]
                        else:
                            TF_x[missingIndices[index]] = xVal
                TF_p = TF_c.dot(np.array(TF_x)[np.newaxis].transpose()) + TF_q # so much work just to transpose a vector
                fitQualityEstimator = np.linalg.norm(TF_S.dot(TF_x) + TF_h)
            if bestFitQualityEstimator == -1 or fitQualityEstimator < bestFitQualityEstimator:
                bestFitQualityEstimator = fitQualityEstimator
                bestTrackParameters = np.ndarray.tolist(TF_p.transpose())[0]

        print "Best track parameters were", [round(param, 3) for param in bestTrackParameters]
        bestTracks.append(bestTrackParameters)

    # print list(set(lostSectorIDs))
    return bestTracks
