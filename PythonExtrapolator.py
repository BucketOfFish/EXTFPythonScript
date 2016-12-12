import numpy as np
from math import floor
from Utilities import *
import MatrixExtraction
import AUXCoordinateExtraction
import DFCoordinateExtraction
import ModuleIDExtraction
import DFHitSSIDCalculator
import AUXExtrapolatedHitsSSIDCalculator

# test code function
def performChecks():

    # crosscheckFileName = 'Data/res_EXPEDCOORDS_T11_v0.txt' # extrapolated coordinates
    # crosscheckFileName = 'Data/res_SSIDS_T11_v0.txt' # global SSIDs
    crosscheckFileName = 'Data/testvector_DF11_2event.dat' # DF data

    with open(crosscheckFileName) as crosscheckFile:
        crosscheckData = [line.strip('\n') for line in crosscheckFile.readlines()]

    # # cross check with "truth" results for extrapolation
    # for line in crosscheckData:
        # print line, regSlice(hexToBin(line), 31, 31), regSlice(hexToBin(line), 15, 15), binToInt(regSlice(hexToBin(line), 10, 0))

if __name__ == "__main__":

    # data formats explained here: https://twiki.cern.ch/twiki/bin/viewauth/Atlas/FastTrackerHardwareDocumentation
    matrixConstantsFileName = 'Data/EXP_T11_21P.txt'
    inputCoordinatesFileName = 'Data/tvec_AUX_tower11_2P40T.txt' # AUX data
    moduleIDDictionaryFileName = 'Data/raw_12LiblHW_32.moduleidmap'
    inputDFFileName = 'Data/testvector_DF11_2event.dat' # DF data

    # open files and read lines
    with open(matrixConstantsFileName) as matrixConstantsFile:
        matrixConstantsData = [line.strip('\n') for line in matrixConstantsFile.readlines()]
    with open(inputCoordinatesFileName) as inputCoordinatesFile:
        inputCoordinatesData = [line.strip('\n') for line in inputCoordinatesFile.readlines()]
    with open(inputDFFileName) as inputDFFile:
        inputDFData = [line.strip('\n') for line in inputDFFile.readlines()]
    with open(moduleIDDictionaryFileName) as moduleIDDictionaryFile:
        moduleIDDictionaryData = [line.strip('\n') for line in moduleIDDictionaryFile.readlines()]

    # convert to binary (easier to work with)
    matrixConstantsData = [hexToBin(hexNumber) for hexNumber in matrixConstantsData]
    inputCoordinatesData = [hexToBin(hexNumber) for hexNumber in inputCoordinatesData]
    inputDFData = [hexToBin(hexNumber) for hexNumber in inputDFData]

    # get extrapolation matrices, input track coordinates, DF coordinates, and local-global module ID dictionary, along with additional data
    matrixValues = MatrixExtraction.extractMatrices(matrixConstantsData)
    hitCoordinates = AUXCoordinateExtraction.extractAUXCoordinates(inputCoordinatesData)
    DFCoordinates = DFCoordinateExtraction.extractDFCoordinates(inputDFData)
    localModuleIDDictionary = ModuleIDExtraction.extractModuleIDDictionary(moduleIDDictionaryData)

    # calculate global SSIDs for DF hits
    DFGlobalSSIDs = DFHitSSIDCalculator.getDFGlobalSSIDs(DFCoordinates, localModuleIDDictionary) # returns vector of (SSID, layer)

    # for every input track, compute the extrapolated global SSIDs
    AUXExtrapolatedGlobalSSIDs = AUXExtrapolatedHitsSSIDCalculator.getAUXExtrapolatedGlobalSSIDs(matrixValues, hitCoordinates, localModuleIDDictionary) # returns vector of (SSID, layer)

    # check if extrapolated hits are among DF hits
    matchedDFHits = []
    for SSID in AUXExtrapolatedGlobalSSIDs:
        if SSID in DFGlobalSSIDs:
            matchedDFHits.append(SSID)
            print "Extrapolated hit at (global SSID, layer)", SSID, "found in DF hits."
        else:
            print "Extrapolated hit at (global SSID, layer)", SSID, "not found."
