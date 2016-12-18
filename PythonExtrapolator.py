import sys
sys.dont_write_bytecode = True # stop generating .pyc files when run

import numpy as np
from math import floor
from Utilities import *
from collections import defaultdict
import ExtrapolatorMatrixExtraction
import TFMatrixExtraction
import AUXCoordinateExtraction
import DFCoordinateExtraction
import ModuleIDExtraction
import DFHitSSIDCalculator
import AUXExtrapolatedHitsSSIDCalculator

# test code function
def performChecks():

    # crosscheckFileName = 'Data/res_EXPEDCOORDS_T11_v0.txt' # extrapolated coordinates
    # crosscheckFileName = 'Data/res_SSIDS_T11_v0.txt' # global SSIDs
    # crosscheckFileName = 'Data/testvector_DF11_2event.dat' # DF data

    with open(crosscheckFileName) as crosscheckFile:
        crosscheckData = [line.strip('\n') for line in crosscheckFile.readlines()]

    # # cross check with "truth" results for extrapolation
    # for line in crosscheckData:
        # print line, regSlice(hexToBin(line), 31, 31), regSlice(hexToBin(line), 15, 15), binToInt(regSlice(hexToBin(line), 10, 0))

if __name__ == "__main__":

    # data formats explained here: https://twiki.cern.ch/twiki/bin/viewauth/Atlas/FastTrackerHardwareDocumentation
    extrapolatorMatrixConstantsFileName = 'Data/EXP_T11_21P.txt' # matrix constants for extrapolator
    inputCoordinatesFileName = 'Data/tvec_AUX_tower11_2P40T.txt' # AUX data
    moduleIDDictionaryFileName = 'Data/raw_12LiblHW_32.moduleidmap' # maps between local module ID, tower and sector ID, and gloabl module ID
    inputDFFileName = 'Data/testvector_DF11_2event.dat' # DF data
    TFMatrixConstantsFileName = 'Data/TFConstants_15sector.txt' # matrix constants for track fitter

    # open files and read lines
    with open(extrapolatorMatrixConstantsFileName) as extrapolatorMatrixConstantsFile:
        extrapolatorMatrixConstantsData = [line.strip('\n') for line in extrapolatorMatrixConstantsFile.readlines()]
    with open(inputCoordinatesFileName) as inputCoordinatesFile:
        inputCoordinatesData = [line.strip('\n') for line in inputCoordinatesFile.readlines()]
    with open(inputDFFileName) as inputDFFile:
        inputDFData = [line.strip('\n') for line in inputDFFile.readlines()]
    with open(moduleIDDictionaryFileName) as moduleIDDictionaryFile:
        moduleIDDictionaryData = [line.strip('\n') for line in moduleIDDictionaryFile.readlines()]
    with open(TFMatrixConstantsFileName) as TFMatrixConstantsFile:
        TFMatrixConstantsData = [line.strip('\n') for line in TFMatrixConstantsFile.readlines()]

    # convert to binary (easier to work with)
    extrapolatorMatrixConstantsData = [hexToBin(hexNumber) for hexNumber in extrapolatorMatrixConstantsData]
    inputCoordinatesData = [hexToBin(hexNumber) for hexNumber in inputCoordinatesData]
    inputDFData = [hexToBin(hexNumber) for hexNumber in inputDFData]
    TFMatrixConstantsData = [hexToBin(hexNumber) for hexNumber in TFMatrixConstantsData]

    # get extrapolation matrices, input track coordinates, DF coordinates, and local-global module ID dictionary, along with additional data
    extrapolatorMatrixValues = ExtrapolatorMatrixExtraction.extractMatrices(extrapolatorMatrixConstantsData)
    hitCoordinates = AUXCoordinateExtraction.extractAUXCoordinates(inputCoordinatesData)
    DFCoordinates = DFCoordinateExtraction.extractDFCoordinates(inputDFData)
    localModuleIDDictionary = ModuleIDExtraction.extractModuleIDDictionary(moduleIDDictionaryData)
    TFMatrixValues = TFMatrixExtraction.extractMatrices(TFMatrixConstantsData) # CHECKPOINT - This module doesn't actually work right now - just copied from ExtrapolatorMatrixExtraction.py

    # calculate global SSIDs for DF hits
    DFGlobalSSIDs = DFHitSSIDCalculator.getDFGlobalSSIDs(DFCoordinates, localModuleIDDictionary) # returns vector of (SSID, layer)

    # for every input track, compute the extrapolated global SSIDs on layers 0, 5, 7, and 11
    AUXExtrapolatedGlobalSSIDs = AUXExtrapolatedHitsSSIDCalculator.getAUXExtrapolatedGlobalSSIDs(extrapolatorMatrixValues, hitCoordinates, localModuleIDDictionary) # returns vector of (SSID, layer)
    
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
    AUXCoordinates = [coord[1] for coord in hitCoordinates] # coordinates of original 8-layer hit
    AUXCoordinates = [[((coord[0], coord[1]), 1), ((coord[2], coord[3]), 2), ((coord[4], coord[5]), 3), (coord[6], 4), (coord[7], 6), (coord[8], 8), (coord[9], 9), (coord[10], 10)] for coord in AUXCoordinates] # organize by layer
    # AUXExtrapolatedCoordinates = AUXExtrapolatedGlobalSSIDs # CHECKPOINT - haven't actually transformed SSIDs into coordinates yet
    AUXExtrapolatedCoordinates = matchedDFExtrapolatedSSIDs # CHECKPOINT - haven't actually transformed SSIDs into coordinates yet
    allCoordinatesInfo = [coord + exCoord for coord, exCoord in zip(AUXCoordinates, AUXExtrapolatedCoordinates)] # coordinates for all 12 layers
    allCoordinatesInfo = [sorted(coordinates, key = lambda coord: coord[1]) for coordinates in allCoordinatesInfo] # sort coordinate info by layer number

    # organization of coordinate info, to make it easier to feed to the track fitter
    for coordinatesInfo in allCoordinatesInfo:
        sortedCoordinates = defaultdict(list)
        for coordinates, layer in coordinatesInfo:
            sortedCoordinates[layer].append(coordinates)
        # sortedCoordinates = map(tuple, sortedCoordinates.values())
        print sortedCoordinates

    # # calculate TF stuff using paper "Linear Fit within Missing-Hit Roads in FTKSim" by Annovi et al.
    # # x, c, q, S, h, C, t defined as in the paper - with TF_ prefix because I don't like single-character variable names
    # S = np.random.rand(16,16) # CHECKPOINT - S is not actually a random matrix
    # for TF_x in allSetsOf12LayerHits:
        # TFMatrixValues
        # if len(TF_x) < fullLength: # estimate missing coordinates in order to minimize fit quality estimator
            # TF_C = blah blah TF_S
            # TF_t = blah
            # TF_x = TF_x + missingCoordinates
        # trackParameters = TF_c * TF_x + TF_q
        # fitQualityEstimator = vectorLength(TF_S * TF_x + TF_h)
