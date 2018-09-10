import numpy as np
import pdb

# calculate TF stuff using paper "Linear Fit within Missing-Hit Roads in FTKSim" by Annovi et al.
# return in form of [[best track], [best track]...], where [best track] = [] if there are too few layers
def fitTracks(trackCandidates, TFConstants):

    bestTracks = []
    fitQualityEstimators = []
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

        ###################################################
        # CHECKPOINT - checking with Markus's spreadsheet #
        ###################################################

        # candidateSet = [[302, 25, 784, 776, 96, 76, 884, 933, 863, 88, 1360, 1144, 1920, 2128, 408, 1969]] # CHECKPOINT
        # candidateSet = [candidate.reverse() for candidate in candidateSet] # CHECKPOINT - making Markus's definitions consistent with mine

        # TF_S = np.array([[-0.011970192193985, -0.005463331937790, 0.004391744732857, 0.638578414916992, 0.506456375122070, -0.110317945480347, 0.408686637878418, -0.048567771911621, -0.025058448314667, -0.072223901748657, -0.032361507415772],
            # [-0.004661947488785, 0.003559343516827, -0.020348191261292, -0.631891250610352, -0.518272399902344, 0.115073442459106, -0.429297447204590, 0.100251197814941, 0.187781810760498, -0.089756488800049, -0.041932582855225],
            # [-0.161185741424561, -0.170917510986328, 0.716627120971680, 0.733295440673828, 0.237679004669189, -0.017349243164063, -0.244256019592285, -0.011081755161285, -0.171190738677979, 0.122377395629883, 0.008669853210449],
            # [0.208407402038574, 0.176784515380859, -0.688440322875977, -0.746520996093750, -0.208485603332520, 0.011892795562744, 0.328866004943848, -0.147583484649658, -0.350955963134766, 0.144258022308350, 0.015386313199997],
            # [-0.233065605163574, -0.241946220397949, 1.047176361083980, -0.530687332153320, -0.073218345642090, 0.061471819877625, 0.060494184494019, 0.044790983200073, 0.173511981964111, 0.089048147201538, 0.058927774429321],
            # [0.198942184448242, 0.230220794677734, -1.044471740722660, 0.536792755126953, 0.077342987060547, -0.024916827678680, -0.161370754241943, 0.159980773925781, 0.338476181030273, 0.081036806106567, 0.054482340812683],
            # [0.183390617370605, 0.325231552124023, 0.035795927047730, -0.552013397216797, 0.896835327148438, -0.135955810546875, -0.008995294570923, -0.066207885742188, -0.009702116250992, -0.199646472930908, 0.013062536716461],
            # [-0.188732147216797, -0.314331054687500, -0.051352024078369, 0.549549102783203, -0.940223693847656, 0.052647471427918, 0.047170758247376, -0.137855529785156, -0.166557788848877, -0.182163715362549, 0.016775965690613],
            # [0.116507530212402, 0.091933250427246, 0.020804107189179, 0.018232047557831, 0.002864845097065, -0.002865657210350, -0.068005084991455, -0.007462590932846, -0.025697648525238, 0.000050149159506, 0.001096561551094],
            # [0.027141153812408, 0.000498075038195, 0.001727670431137, 0.003785841166973, 0.017502963542938, 0.089937686920166, 0.014615863561630, 0.118396759033203, -0.024175345897675, 0.009743958711624, -0.025810122489929],
            # [-0.191000461578369, -0.034891963005066, -0.052824497222900, -0.014543026685715, 0.040428638458252, 0.004805743694305, -0.040633320808411, 0.002381823956966, -0.017161369323731, -0.000597676262259, 0.000798705965281],
            # [-0.044907569885254, 0.006960034370422, 0.000730289146304, -0.009333610534668, -0.031403660774231, -0.188178539276123, -0.027258157730103, -0.091335773468018, 0.034627079963684, 0.018095493316650, -0.017058670520783],
            # [0.107853174209595, -0.184167861938477, -0.020876884460449, -0.013525336980820, 0.020236670970917, -0.015377938747406, 0.000236003659666, 0.002321004867554, 0.002020448446274, -0.000892987474799, 0.000015182275092],
            # [0.024304628372192, -0.023129582405090, -0.014508724212647, 0.015051573514938, 0.046076416969299, 0.201207160949707, -0.004398316144943, -0.096892833709717, 0.021259903907776, 0.000298156403005, 0.006996691226959],
            # [-0.016458988189697, 0.085253477096558, 0.028198897838593, 0.006846219301224, -0.029269039630890, 0.003847919404507, 0.056146860122681, 0.002516761422157, 0.019404768943787, -0.001201495528221, -0.000667881220579],
            # [-0.004433304071426, 0.013941973447800, 0.012529909610748, -0.010214924812317, -0.029214918613434, -0.103371143341064, 0.017020225524902, 0.090527296066284, -0.030548334121704, -0.012579888105393, 0.022223472595215]]).transpose() # CHECKPOINT
        # TF_h = np.array([-46.852661132812500, 310.626953125000000, 54.133178710937500, -39.045288085937500, -71.503173828125000, 90.035644531250000, -31.360839843750000, 416.453125000000000, 536.478515625000000, 138.770507812500000, -90.362548828125000]).transpose() # CHECKPOINT
        # TF_c = np.array([[0.000676380470395, 0.000504646450281, -0.000037204357795, 0.000004210363841, 0.000000424168320],
            # [0.000909602269530, -0.001212112605572, 0.000048897694796, -0.000067195156589, -0.000001389587851],
            # [0.000884583219886, 0.002654589712620, 0.000004656612873, 0.000021635962185, 0.000000989351975],
            # [-0.003282628953457, -0.000078214332461, -0.000067434040830, 0.000075640389696, 0.000000537378583],
            # [-0.001932132989168, -0.004524081945419, 0.000030950759538, 0.000083831138909, 0.000000344901309],
            # [0.002637930214405, 0.000774133950472, 0.000079918187112, -0.000123600941151, -0.000001194552169],
            # [0.000041279708967, 0.002002589404583, -0.000070428475738, 0.000007061797078, 0.000000339311555],
            # [0.000541694462299, 0.001182444393635, -0.000017460610252, -0.000023562228307, -0.000000464988261],
            # [0.000236641149968, -0.006157770752907, 0.000165541656315, -0.000007097842172, 0.000000029064950],
            # [-0.000404954887927, -0.001066815108061, 0.000014491117327, 0.000022827764042, 0.000000550837285],
            # [0.000217093620449, -0.004995644092560, 0.000161160714924, -0.000006243149983, 0.000000010799567],
            # [-0.000993389636278, -0.000204783864319, 0.000022401334718, 0.000013851473341, -0.000000443041245],
            # [-0.000267230905592, 0.000758212059736, 0.000098791671917, 0.000008973001968, 0.000000004040331],
            # [-0.007218480110168, 0.001816727221012, -0.000037360121496, 0.000228319317102, 0.000000158686362],
            # [0.000136602204293, 0.022194266319275, -0.000264351256192, -0.000004917092156, -0.000000024760993],
            # [0.014632701873779, 0.000364933162928, 0.000004984016414, -0.000270121730864, -0.000000200557224]]).transpose() # CHECKPOINT
        # TF_q = np.array([-11.147644042968800, -30.406311035156200, -0.676544189453125, 1.763809204101560, -0.000823061913252]).transpose() # CHECKPOINT

        # # Making Markus's definitions consistent with mine
        # TF_S = np.array(TF_S.tolist().reverse())
        # TF_h = np.array(TF_h.tolist().reverse())
        # TF_c = np.array(TF_c.tolist().reverse())
        # TF_q = np.array(TF_q.tolist().reverse())

        # print "TF_S", TF_S
        # print "TF_h", TF_h
        # print "TF_c", TF_c
        # print "TF_q", TF_q

        ###################################################
        # CHECKPOINT - checking with Markus's spreadsheet #
        ###################################################

        nCandidates = len(candidateSet)
        missingIndices = np.where(np.array(candidateSet[0]) == -1)[0]
        measuredIndices = np.where(np.array(candidateSet[0]) != -1)[0]
        nMissingIndices = len(missingIndices)
        nIBLLayers = sum(coord != -1 for coord in candidateSet[0][:8]) / 2 # IBL layers we have hits for
        nSCTLayers = sum(coord != -1 for coord in candidateSet[0][8:]) # SCT layers we have hits for
        nLayers = nIBLLayers + nSCTLayers

        bestTrackParameters = []
        bestFitQualityEstimator = -1
        bestTrack = None

        if nLayers < 11: # not enough layers
            print "Not enough layers - fit terminated" # CHECKPOINT
            continue
        else:
            # print "Fitting..." # CHECKPOINT
            for trackCandidate in candidateSet:
                TF_x = np.array(trackCandidate)
                if nLayers < 12: # missing layers
                    # print "TF_x", TF_x, "missing indices", missingIndices # CHECKPOINT
                    # print "TF_S", TF_S # CHECKPOINT
                    missingTF_S = TF_S[:, missingIndices]
                    measuredTF_S = TF_S[:, measuredIndices]
                    measuredTF_x = TF_x[measuredIndices]
                    TF_C = missingTF_S.transpose().dot(missingTF_S)
                    # print "TF_C", TF_C # CHECKPOINT
                    TF_t = - missingTF_S.transpose().dot(TF_h).transpose() - missingTF_S.transpose().dot(measuredTF_S.dot(measuredTF_x))
                    # print "TF_t", TF_t # CHECKPOINT
                    missingTF_x = np.linalg.inv(TF_C).dot(TF_t.transpose())
                    # print "invC", np.linalg.inv(TF_C) # CHECKPOINT
                    # print "missingTF_x", missingTF_x # CHECKPOINT
                    for index, xVal in enumerate(missingTF_x):
                        if isinstance(xVal, list):
                            TF_x[missingIndices[index]] = xVal[0]
                        else:
                            TF_x[missingIndices[index]] = -xVal
                    # print "final TF_x", TF_x # CHECKPOINT
                # a = TF_c.dot(np.array(TF_x)[np.newaxis].transpose()) # CHECKPOINT
                # print(a) # CHECKPOINT
                # print(TF_q) # CHECKPOINT
                # print(a.flatten() + TF_q) # CHECKPOINT
                TF_p = TF_c.dot(np.array(TF_x)[np.newaxis].transpose()).flatten() + TF_q # so much work just to transpose a vector
                fitQualityEstimator = pow(np.linalg.norm(TF_S.dot(TF_x) + TF_h), 2)
                if bestFitQualityEstimator == -1 or fitQualityEstimator < bestFitQualityEstimator:
                    # print "Found better fit!" # CHECKPOINT
                    bestFitQualityEstimator = fitQualityEstimator
                    bestTrackParameters = np.ndarray.tolist(TF_p)
                    bestTrack = trackCandidate

        if bestFitQualityEstimator > 40: # not good enough - do recovery fits
            # not very elegant code - basically just copy-pasted the above - should clean up (but probably won't)
            # print "Fitting recovery tracks..." # CHECKPOINT
            # print TF_S # CHECKPOINT
            moreTrackCandidates = []
            for trackCandidate in candidateSet:
                for dropLayers in [[0, 1], [8], [10], [14]]: # drop each of these separately (pixel layer 0, SCT layers 5, 7, 11)
                    candidateCopy = trackCandidate[:]
                    for layer in dropLayers:
                        candidateCopy[layer] = -1
                    moreTrackCandidates.append(candidateCopy)
            for trackCandidate in moreTrackCandidates:
                TF_x = np.array(trackCandidate)
                missingIndices = np.where(np.array(trackCandidate) == -1)[0]
                measuredIndices = np.where(np.array(trackCandidate) != -1)[0]
                nMissingIndices = len(missingIndices)
                nIBLLayers = sum(coord != -1 for coord in trackCandidate[:8]) / 2 # IBL layers we have hits for
                nSCTLayers = sum(coord != -1 for coord in trackCandidate[8:]) # SCT layers we have hits for
                nLayers = nIBLLayers + nSCTLayers
                if nLayers < 11: # not enough layers
                    continue
                else:
                    if nLayers < 12: # missing layers
                        # print "TF_x", TF_x, "missing indices", missingIndices # CHECKPOINT
                        # print "TF_S", TF_S # CHECKPOINT
                        missingTF_S = TF_S[:, missingIndices]
                        measuredTF_S = TF_S[:, measuredIndices]
                        measuredTF_x = TF_x[measuredIndices]
                        TF_C = missingTF_S.transpose().dot(missingTF_S)
                        # print "TF_C", TF_C # CHECKPOINT
                        # print "Missing TF_S", missingTF_S.transpose()
                        # print "TF_h", TF_h
                        # print "Measured TF_S", measuredTF_S
                        # print "Measured TF_x", measuredTF_x
                        TF_t = - missingTF_S.transpose().dot(TF_h).transpose() - missingTF_S.transpose().dot(measuredTF_S.dot(measuredTF_x))
                        # print "TF_t", TF_t # CHECKPOINT
                        missingTF_x = np.linalg.inv(TF_C).dot(TF_t.transpose())
                        # print "invC", np.linalg.inv(TF_C) # CHECKPOINT
                        # print "missingTF_x", missingTF_x # CHECKPOINT
                        for index, xVal in enumerate(missingTF_x):
                            if isinstance(xVal, list):
                                TF_x[missingIndices[index]] = xVal[0]
                            else:
                                TF_x[missingIndices[index]] = -xVal
                        # print "final TF_x", TF_x # CHECKPOINT
                    # a = TF_c.dot(np.array(TF_x)[np.newaxis].transpose()) # CHECKPOINT
                    # print(a) # CHECKPOINT
                    # print(TF_q) # CHECKPOINT
                    # print(a.flatten() + TF_q) # CHECKPOINT
                    TF_p = TF_c.dot(np.array(TF_x)[np.newaxis].transpose()).flatten() + TF_q # so much work just to transpose a vector
                    fitQualityEstimator = pow(np.linalg.norm(TF_S.dot(TF_x) + TF_h), 2)
                    # print "Recovery track of", [round(param, 3) for param in TF_x], "with parameters", [round(param, 3) for param in np.ndarray.tolist(TF_p)], "and a chi2 value of", fitQualityEstimator
                    if bestFitQualityEstimator == -1 or fitQualityEstimator < bestFitQualityEstimator:
                        # print "Found better fit!" # CHECKPOINT
                        bestFitQualityEstimator = fitQualityEstimator
                        bestTrackParameters = np.ndarray.tolist(TF_p)
                        bestTrack = trackCandidate

        print "Best track was", bestTrack
        print "Best track parameters were", [round(param, 3) for param in bestTrackParameters], "with a chi2 value of", bestFitQualityEstimator
        bestTracks.append(bestTrackParameters)
        fitQualityEstimators.append(bestFitQualityEstimator)

    # print list(set(lostSectorIDs))
    return zip(fitQualityEstimators, bestTracks)
