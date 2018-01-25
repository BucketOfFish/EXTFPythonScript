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

if __name__ == "__main__":

    # execfile("Options/Stream3_Tower22_1Event.py")
    execfile("Options/Stream3_Tower22_1Event_noLoop.py")

    #################
    # Extrapolation #
    #################

    # open files and read lines
    with open(extrapolatorConstants_FileName) as extrapolatorConstantsFile:
        extrapolatorConstants_Lines = [line.strip('\n') for line in extrapolatorConstantsFile.readlines()]
    with open(inputAUXData_FileName) as inputAUXDataFile:
        inputAUXData_Lines = [line.strip('\n') for line in inputAUXDataFile.readlines()]
    with open(moduleIDDictionary_FileName) as moduleIDDictionaryFile:
        moduleIDDictionary_Lines = [line.strip('\n') for line in moduleIDDictionaryFile.readlines()]

    # convert to binary (easier to work with)
    extrapolatorConstants_Lines = [hexToBin(hexNumber) for hexNumber in extrapolatorConstants_Lines]
    if shiftBitAUX:
        inputAUXData_Lines = [hexToBin(shiftBackToFront(hexNumber)) for hexNumber in inputAUXData_Lines]
    else:
        inputAUXData_Lines = [hexToBin(hexNumber) for hexNumber in inputAUXData_Lines]

    # convert input lines to usable data
    extrapolatorConstants = ExtrapolatorConstantsExtraction.extractConstants(extrapolatorConstants_Lines)
    inputAUXData = AUXDataExtraction.extractAUXData(inputAUXData_Lines) # 8 layer hit coordinates
    moduleIDDictionary = ModuleIDExtraction.extractModuleIDDictionary(moduleIDDictionary_Lines)

    # for every input AUX track, compute the (expanded) extrapolated global SSIDs on layers 0, 5, 7, and 11
    extrapolatedGlobalSSIDs = Extrapolator.getExtrapolatedGlobalSSIDs(extrapolatorConstants, inputAUXData, tower, moduleIDDictionary)

    #################
    # Hits Matching #
    #################

    with open(inputDFData_FileName) as inputDFDataFile:
        inputDFData_Lines = [line.strip('\n') for line in inputDFDataFile.readlines()]
    if shiftBitDF:
        inputDFData_Lines = [hexToBin(shiftBackToFront(hexNumber)) for hexNumber in inputDFData_Lines]
    else:
        inputDFData_Lines = [hexToBin(hexNumber) for hexNumber in inputDFData_Lines]

    # calculate global SSIDs for DF hits
    inputDFData = DFDataExtraction.extractDFData(inputDFData_Lines)
    DFGlobalSSIDs = DFHitSSIDCalculator.getDFGlobalSSIDs(inputDFData, moduleIDDictionary, tower)

    # based on extrapolated SSIDs from AUX data, and SSIDs of DF hits, and given the original 8-layer hits, find all combinations of possible 12-layer hits for tracks
    trackCandidates = TrackCandidatesFinder.listTrackCandidates(inputAUXData, extrapolatedGlobalSSIDs, DFGlobalSSIDs)

    print "Track candidates in the form [([track candidates for 8L input], track sector ID), ([track candidates], sector ID)...], where [track candidates] = [[16 hit coords], [16 hit coords]...], and layer 0 is the first hit coords"
    for candidate in trackCandidates:
        print candidate 

    #################
    # Track Fitting #
    #################

    # with open(TFConstants_FileName) as TFConstantsFile:
        # TFConstantsData = [line.strip('\n') for line in TFConstantsFile.readlines()]
    # TFConstantsData = [hexToBin(hexNumber) for hexNumber in TFConstantsData]
    # TFConstants = TFConstantsExtraction.extractConstants(TFConstantsData)

    # # calculates best track fit from track candidates
    # bestTracks = TrackFitter.fitTracks(trackCandidates, TFConstants)

    # print "\n----------------------------------------"
    # print "Printing chi2 values and parameters for best-fit tracks:"
    # for track in bestTracks:
        # print track[0], ",", [round(param, 3) for param in track[1]]
