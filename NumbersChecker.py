# test code function
def checkNumbers():

    # crosscheckFileName = 'Data/res_EXPEDCOORDS_T11_v0.txt' # extrapolated coordinates
    # crosscheckFileName = 'Data/res_SSIDS_T11_v0.txt' # global SSIDs
    # crosscheckFileName = 'Data/testvector_DF11_2event.dat' # DF data

    with open(crosscheckFileName) as crosscheckFile:
        crosscheckData = [line.strip('\n') for line in crosscheckFile.readlines()]

    # # cross check with "truth" results for extrapolation
    # for line in crosscheckData:
        # print line, regSlice(hexToBin(line), 31, 31), regSlice(hexToBin(line), 15, 15), binToInt(regSlice(hexToBin(line), 10, 0))
