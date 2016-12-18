import sys
sys.dont_write_bytecode = True # stop generating .pyc files when run

import numpy as np
from math import floor
from Utilities import *
import ExtrapolatorMatrixExtraction
import TFMatrixExtraction
import AUXCoordinateExtraction
import DFCoordinateExtraction
import ModuleIDExtraction
import DFHitSSIDCalculator
import AUXExtrapolatedHitsSSIDCalculator
import HitSorter
import NumbersChecker
import TrackFitter

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
        inputAUXData = [line.strip('\n') for line in inputCoordinatesFile.readlines()]
    with open(inputDFFileName) as inputDFFile:
        inputDFData = [line.strip('\n') for line in inputDFFile.readlines()]
    with open(moduleIDDictionaryFileName) as moduleIDDictionaryFile:
        moduleIDDictionaryData = [line.strip('\n') for line in moduleIDDictionaryFile.readlines()]
    with open(TFMatrixConstantsFileName) as TFMatrixConstantsFile:
        TFMatrixConstantsData = [line.strip('\n') for line in TFMatrixConstantsFile.readlines()]

    # convert to binary (easier to work with)
    extrapolatorMatrixConstantsData = [hexToBin(hexNumber) for hexNumber in extrapolatorMatrixConstantsData]
    inputAUXData = [hexToBin(hexNumber) for hexNumber in inputAUXData]
    inputDFData = [hexToBin(hexNumber) for hexNumber in inputDFData]
    TFMatrixConstantsData = [hexToBin(hexNumber) for hexNumber in TFMatrixConstantsData]

    # get extrapolation matrices, input track coordinates, DF coordinates, and local-global module ID dictionary, along with additional data
    extrapolatorMatrixValues = ExtrapolatorMatrixExtraction.extractMatrices(extrapolatorMatrixConstantsData)
    AUXHits = AUXCoordinateExtraction.extractAUXHits(inputAUXData)
    DFCoordinates = DFCoordinateExtraction.extractDFCoordinates(inputDFData)
    localModuleIDDictionary = ModuleIDExtraction.extractModuleIDDictionary(moduleIDDictionaryData)
    TFMatrixValues = TFMatrixExtraction.extractMatrices(TFMatrixConstantsData) # CHECKPOINT - This module doesn't actually work right now - just copied from ExtrapolatorMatrixExtraction.py

    # calculate global SSIDs for DF hits
    DFGlobalSSIDs = DFHitSSIDCalculator.getDFGlobalSSIDs(DFCoordinates, localModuleIDDictionary) # returns vector of (SSID, layer)

    # for every input track, compute the extrapolated global SSIDs on layers 0, 5, 7, and 11
    AUXExtrapolatedGlobalSSIDs = AUXExtrapolatedHitsSSIDCalculator.getAUXExtrapolatedGlobalSSIDs(extrapolatorMatrixValues, AUXHits, localModuleIDDictionary) # returns vector of (SSID, layer)
    
    # get all combinations of 12-layer hits for track fitting
    trackCandidates = HitSorter.listTrackCandidates(AUXHits, AUXExtrapolatedGlobalSSIDs, DFGlobalSSIDs)

    # calculates best track fit from track candidates
    bestTrack = TrackFitter.fitTracks(trackCandidates)
