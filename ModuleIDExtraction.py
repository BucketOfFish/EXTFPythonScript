import numpy as np
from Utilities import *

# given columns containing tower, layer, global module ID, and local module ID, create a dictionary
# return in form of dictionary where (tower, layer, global module ID) is the key and local module ID is the value
def extractModuleIDDictionary(moduleIDDictionaryData):

    # extracted values
    localModuleIDs = []
    localModuleIDInfo = []

    # # read through each line of the file
    # for line in moduleIDDictionaryData:

        # values = line.split("\t")
        # tower = int(values[0])
        # layer = int(values[1])
        # globalModuleID = int(values[2])
        # localModuleID = int(values[3])
        # localModuleIDs.append(localModuleID)
        # localModuleIDInfo.append((tower, layer, globalModuleID))

    # return dict(zip(localModuleIDInfo, localModuleIDs)) # dictionary where module ID info tuples are keys, for getting the module local ID

    for line in moduleIDDictionaryData:
        # ssmap_addr = binToInt(regSlice(line, 22, 9))
        tower = binToInt(regSlice(line, 22, 22))
        module_hashid = binToInt(regSlice(line, 21, 9)) # global module ID
        ssmap_din = binToInt(regSlice(line, 8, 0)) # local module ID
        layer = 0
        localModuleIDs.append(ssmap_din)
        localModuleIDInfo.append((tower, layer, module_hashid))

    return dict(zip(localModuleIDInfo, localModuleIDs)) # dictionary where module ID info tuples are keys, for getting the module local ID
