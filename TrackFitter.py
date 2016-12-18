import numpy as np

# calculate TF stuff using paper "Linear Fit within Missing-Hit Roads in FTKSim" by Annovi et al.
def fitTracks(trackCandidates, TFConstants):

    # x, c, q, S, h, C, t defined as in the paper - with TF_ prefix because I don't like single-character variable names
    TF_c = np.random.rand(5,16) # CHECKPOINT - extract from TFConstants
    TF_q = np.random.rand(5,1) # CHECKPOINT - extract from TFConstants
    TF_S = np.random.rand(16,16) # CHECKPOINT - extract from TFConstants
    TF_h = np.random.rand(16,1) # CHECKPOINT - extract from TFConstants
    # TF_c = np.array(matrixValues[sectorID][0])
    # TF_q = np.array(matrixValues[sectorID][1])
    # TF_S = np.array(matrixValues[sectorID][2])
    # TF_h = np.array(matrixValues[sectorID][3])

    bestTracks = []

    for candidateSet in trackCandidates:

        nCandidates = len(candidateSet)
        nIBLLayers = sum(coord != -1 for coord in candidateSet[0][:8]) / 2 # IBL layers we have hits for
        nSCTLayers = sum(coord != -1 for coord in candidateSet[0][8:]) # SCT layers we have hits for
        nLayers = nIBLLayers + nSCTLayers

        bestTrackParameters = []
        bestFitQualityEstimator = -1

        if nLayers < 11: # CHECKPOINT - not enough layers, but check if 11 is the limit
            pass
        else:
            for trackCandidate in candidateSet:
                TF_x = np.array(trackCandidate)
                if nLayers == 12: # have all the layers
                    TF_p = TF_c.dot(TF_x) + TF_q
                    fitQualityEstimator = np.linalg.norm(TF_S.dot(TF_x) + TF_h)
                else: # missing some layers
                    # if len(TF_x) < fullLength: # estimate missing coordinates in order to minimize fit quality estimator
                        # TF_C = blah blah TF_S
                        # TF_t = blah
                        # TF_x = TF_x + missingCoordinates
                    # trackParameters = TF_c * TF_x + TF_q
                    # extrapolatedCoordinates = vector + matrix.dot(coordinates) # perform matrix extrapolation - this gives [IBL_phi IBL_eta SCT SCT SCT]
            if bestFitQualityEstimator == -1 or fitQualityEstimator < bestFitQualityEstimator:
                bestFitQualityEstimator = fitQualityEstimator
                bestTrackParameters = TF_p

        bestTracks.append((bestTrackParameters, fitQualityEstimator))

    return bestTracks

# to do:
# - solve for TF_p and chi^2 for tracks with missing hits
