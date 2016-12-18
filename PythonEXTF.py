import sys
sys.dont_write_bytecode = True # stop generating .pyc files when run

from Utilities import *
import ExtrapolatorConstantsExtraction
import AUXDataExtraction
import ModuleIDExtraction
import Extrapolator
import DFDataExtraction
import DFHitSSIDCalculator
import TrackCandidatesFinder
import TFConstantsExtraction
import TrackFitter
import NumbersChecker # for printing stuff during debugging

if __name__ == "__main__":

    #################
    # Extrapolation #
    #################

    extrapolatorConstants_FileName = 'Data/EXP_T11_21P.txt' # matrix and vector constants for extrapolator
    inputAUXData_FileName = 'Data/tvec_AUX_tower11_2P40T.txt' # AUX input data
    moduleIDDictionary_FileName = 'Data/raw_12LiblHW_32.moduleidmap' # maps between local module ID, tower and sector ID, and gloabl module ID

    # open files and read lines
    with open(extrapolatorConstants_FileName) as extrapolatorConstantsFile:
        extrapolatorConstants_Lines = [line.strip('\n') for line in extrapolatorConstantsFile.readlines()]
    with open(inputAUXData_FileName) as inputAUXDataFile:
        inputAUXData_Lines = [line.strip('\n') for line in inputAUXDataFile.readlines()]
    with open(moduleIDDictionary_FileName) as moduleIDDictionaryFile:
        moduleIDDictionary_Lines = [line.strip('\n') for line in moduleIDDictionaryFile.readlines()]

    # convert to binary (easier to work with)
    extrapolatorConstants_Lines = [hexToBin(hexNumber) for hexNumber in extrapolatorConstants_Lines]
    inputAUXData_Lines = [hexToBin(hexNumber) for hexNumber in inputAUXData_Lines]

    # convert input lines to usable data
    extrapolatorConstants = ExtrapolatorConstantsExtraction.extractConstants(extrapolatorConstants_Lines)
    inputAUXData = AUXDataExtraction.extractAUXData(inputAUXData_Lines) # 8 layer hit coordinates
    moduleIDDictionary = ModuleIDExtraction.extractModuleIDDictionary(moduleIDDictionary_Lines)

    # for every input AUX track, compute the (expanded) extrapolated global SSIDs on layers 0, 5, 7, and 11
    extrapolatedGlobalSSIDs = Extrapolator.getExtrapolatedGlobalSSIDs(extrapolatorConstants, inputAUXData, moduleIDDictionary)

    #################
    # Hits Matching #
    #################

    inputDFData_FileName = 'Data/testvector_DF11_2event.dat' # DF data
    with open(inputDFData_FileName) as inputDFDataFile:
        inputDFData_Lines = [line.strip('\n') for line in inputDFDataFile.readlines()]
    inputDFData_Lines = [hexToBin(hexNumber) for hexNumber in inputDFData_Lines]

    # calculate global SSIDs for DF hits
    inputDFData = DFDataExtraction.extractDFData(inputDFData_Lines)
    DFGlobalSSIDs = DFHitSSIDCalculator.getDFGlobalSSIDs(inputDFData, moduleIDDictionary)

    # based on extrapolated SSIDs from AUX data, and SSIDs of DF hits, and given the original 8-layer hits, find all combinations of possible 12-layer hits for tracks
    trackCandidates = TrackCandidatesFinder.listTrackCandidates(inputAUXData, extrapolatedGlobalSSIDs, DFGlobalSSIDs)

    #################
    # Track Fitting #
    #################

    TFConstants_FileName = 'Data/TFConstants_15sector.txt' # matrix and vector constants for track fitter
    with open(TFConstants_FileName) as TFConstantsFile:
        TFConstantsData = [line.strip('\n') for line in TFConstantsFile.readlines()]
    TFConstantsData = [hexToBin(hexNumber) for hexNumber in TFConstantsData]

    TFConstants = TFConstantsExtraction.extractConstants(TFConstantsData) # CHECKPOINT - This module doesn't actually work right now - just copied from ExtrapolatorMatrixExtraction.py

    # calculates best track fit from track candidates
    bestTrack = TrackFitter.fitTracks(trackCandidates, TFConstants)
