from Utilities import *

# test code - for printing stuff during debugging
def checkNumbers():

    # crosscheckFileName = 'Data/res_EXPEDCOORDS_T11_v0.txt' # extrapolated coordinates
    # crosscheckFileName = 'Data/res_SSIDS_T11_v0.txt' # global SSIDs
    # crosscheckFileName = 'Data/testvector_DF11_2event.dat' # DF data
    crosscheckFileName = 'Data/TFConstants_15sector.txt' # matrix and vector constants for track fitter

    with open(crosscheckFileName) as crosscheckFile:
        crosscheckData = [line.strip('\n') for line in crosscheckFile.readlines()]

    for line in crosscheckData:
        # convert hex file to binary
        print line, hexToBin(line)
        # # cross check with "truth" results for extrapolation
        # print line, regSlice(hexToBin(line), 31, 31), regSlice(hexToBin(line), 15, 15), binToInt(regSlice(hexToBin(line), 10, 0))

if __name__ == "__main__":

    checkNumbers()
