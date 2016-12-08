import numpy as np
from Utilities import *

# given columns containing tower, layer, global module ID, and local module ID, create a dictionary
def extractModuleIDDictionary(moduleIDDictionaryData):

    # extracted values
    localModuleIDs = []
    localModuleIDInfo = []

    # read through each line of the file
    for line in moduleIDDictionaryData:

        values = line.split("\t")
        tower = int(values[0])
        layer = int(values[1])
        globalModuleID = int(values[2])
        localModuleID = int(values[3])
        localModuleIDs.append(localModuleID)
        localModuleIDInfo.append((tower, layer, globalModuleID))

    return dict(zip(localModuleIDInfo, localModuleIDs)) # dictionary where module ID info tuples are keys, for getting the module local ID
