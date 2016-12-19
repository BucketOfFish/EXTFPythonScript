import numpy as np

# calculate TF stuff using paper "Linear Fit within Missing-Hit Roads in FTKSim" by Annovi et al.
# return in form of [[best track], [best track]...], where [best track] = [] if there are too few layers
def fitTracks(trackCandidates, TFConstants):

    # x, c, q, S, h, C, t defined as in the paper - with TF_ prefix because I don't like single-character variable names
    TF_c = np.random.rand(5,16) # CHECKPOINT - extract from TFConstants
    TF_q = np.random.rand(5,1) # CHECKPOINT - extract from TFConstants
    TF_S = np.random.rand(11,16) # CHECKPOINT - extract from TFConstants
    TF_h = np.random.rand(11,1) # CHECKPOINT - extract from TFConstants
    # TF_c = np.array(matrixValues[sectorID][0])
    # TF_q = np.array(matrixValues[sectorID][1])
    # TF_S = np.array(matrixValues[sectorID][2])
    # TF_h = np.array(matrixValues[sectorID][3])

    bestTracks = []

    for candidateSet in trackCandidates:

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
            pass
        else:
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
                        TF_x[missingIndices[index]] = xVal[0]
                TF_p = TF_c.dot(np.array(TF_x)[np.newaxis].transpose()) + TF_q # so much work just to transpose a vector
                fitQualityEstimator = np.linalg.norm(TF_S.dot(TF_x) + TF_h)
            if bestFitQualityEstimator == -1 or fitQualityEstimator < bestFitQualityEstimator:
                bestFitQualityEstimator = fitQualityEstimator
                bestTrackParameters = np.ndarray.tolist(TF_p.transpose())[0]

        bestTracks.append(bestTrackParameters)

    return bestTracks
