import sys, pdb  # NOQA
import Utilities as U
import ExtrapolatorConstantsExtraction
import AUXDataExtraction
import ModuleIDExtraction
import Extrapolator
import DFDataExtraction
import DFHitSSIDCalculator
import TrackCandidatesFinder
import TFConstantsExtraction
import TrackFitter
import HitWarrior

sys.dont_write_bytecode = True  # stop generating .pyc files when run # NOQA


def process_one_event(inputAUXData, inputDFData, extrapolatorConstants, moduleIDDictionary, TFConstants):

    print("AUX tracks (sectorID, 11 coordinates)")
    for track in inputAUXData:
        print(track)
    print("")

    print("DF hits (global module ID, hit coordinates)")
    for hits in inputDFData:
        print(hits, end=' ')
    print("\n")

    #################
    # Extrapolation #
    #################

    # for every input AUX track, compute the (expanded) extrapolated global SSIDs on layers 0, 5, 7, and 11
    extrapolatedGlobalSSIDs = Extrapolator.getExtrapolatedGlobalSSIDs(extrapolatorConstants, inputAUXData, moduleIDDictionary, tower)

    print("extrapolated global SSIDs")
    expTrackSSIDs = [[i[0] for i in j] for j in extrapolatedGlobalSSIDs]
    for global_SSIDs_for_track in expTrackSSIDs:
        print(global_SSIDs_for_track)
    print("")

    #################
    # Hits Matching #
    #################

    # calculate global SSIDs from DF hit coordinates - has temporary fix to ignore SSID=0 hits
    DFGlobalSSIDs = DFHitSSIDCalculator.getDFGlobalSSIDs(inputDFData, moduleIDDictionary, tower)

    print("DF SSIDs")
    DFSSIDs = [i[0] for i in DFGlobalSSIDs]
    print(sorted(set(DFSSIDs)))
    print("")
    print("SSID matches for each track")
    matchedTrackSSIDs = []
    for track in expTrackSSIDs:
        matchedTrackSSIDs.append(list(set.intersection(set(track), DFSSIDs)))
        print(matchedTrackSSIDs[-1])
    print("")

    ####################
    # Track Candidates #
    ####################

    # based on extrapolated SSIDs from AUX data, and SSIDs of DF hits, and given the original 8-layer hits, find all combinations of possible 12-layer hits for tracks
    trackCandidates = TrackCandidatesFinder.listTrackCandidates(inputAUXData, extrapolatedGlobalSSIDs, DFGlobalSSIDs)

    print("Track candidates in the form [([track candidates for 8L input], track sector ID), ([track candidates], sector ID)...], where [track candidates] = [[16 hit coords], [16 hit coords]...], and layer 0 is the first hit coords")
    for track in trackCandidates:
        print(track)
    print("")

    #################
    # Track Fitting #
    #################

    # calculates best track fit from track candidates
    # not sure if this code is correct - I know literally nothing about TrackFitter
    bestTracks = TrackFitter.fitTracks(trackCandidates, TFConstants)

    print("Best-fit tracks with fit parameters and chi2 values:")
    for track in bestTracks:
        print(track[0], ",", [round(param, 3) for param in track[1]], ",", round(track[2], 3))
    print("")

    ###############
    # Hit Warrior #
    ###############

    # remove heavily-overlapping tracks
    uniqueTracks = HitWarrior.overlapRemoval(bestTracks)

    print("Removing overlapping tracks leaves:")
    for track in uniqueTracks:
        print(track[0])
    print("")


if __name__ == "__main__":

    exec(open("Options/DefaultOptions.py").read())
    print("Loading constants\n")

    # extrapolation constants
    with open(extrapolatorConstants_FileName) as extrapolatorConstantsFile:
        extrapolatorConstants_Lines = [line.strip('\n') for line in extrapolatorConstantsFile.readlines()]
    extrapolatorConstants_Lines = [U.hexToBin(hexNumber) for hexNumber in extrapolatorConstants_Lines]
    extrapolatorConstants = ExtrapolatorConstantsExtraction.extractConstants(extrapolatorConstants_Lines)

    # local-global module ID dictionary
    with open(moduleIDDictionary_FileName) as moduleIDDictionaryFile:
        moduleIDDictionary_Lines = [line.strip('\n') for line in moduleIDDictionaryFile.readlines()]
    moduleIDDictionary = ModuleIDExtraction.extractModuleIDDictionary(moduleIDDictionary_Lines)

    # track fitting constants
    with open(TFConstants_FileName) as TFConstantsFile:
        TFConstantsData = [line.strip('\n') for line in TFConstantsFile.readlines()]
    TFConstantsData = [U.hexToBin(hexNumber) for hexNumber in TFConstantsData]
    TFConstants = TFConstantsExtraction.extractConstants(TFConstantsData)

    # AUX stream
    with open(inputAUXData_FileName) as inputAUXDataFile:
        inputAUXData_Lines = [line.strip('\n') for line in inputAUXDataFile.readlines()]
    if shiftBitAUX:
        inputAUXData_Lines = [U.hexToBin(shiftBackToFront(hexNumber)) for hexNumber in inputAUXData_Lines]
    else:
        inputAUXData_Lines = [U.hexToBin(hexNumber) for hexNumber in inputAUXData_Lines]
    AUXDataEvents = list(AUXDataExtraction.extractAUXData(inputAUXData_Lines))  # 8 layer hit coordinates

    # DF stream
    with open(inputDFData_FileName) as inputDFDataFile:
        inputDFData_Lines = [line.strip('\n') for line in inputDFDataFile.readlines()]
    if shiftBitDF:
        inputDFData_Lines = [U.hexToBin(shiftBackToFront(hexNumber)) for hexNumber in inputDFData_Lines]
    else:
        inputDFData_Lines = [U.hexToBin(hexNumber) for hexNumber in inputDFData_Lines]
    DFDataEvents = list(DFDataExtraction.extractDFData(inputDFData_Lines))

    for (inputAUXData, inputDFData) in zip(AUXDataEvents, DFDataEvents):
        print("Processing an event")
        print("")
        DFHits = process_one_event(list(inputAUXData), list(inputDFData), extrapolatorConstants, moduleIDDictionary, TFConstants)
        input("Press Enter to continue...")
        print("")
