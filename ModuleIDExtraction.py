def extractModuleIDDictionary(moduleIDDictionaryData):
    '''Given columns containing tower, layer, global module ID, and local module ID, create a dictionary and
    return in form where (tower, layer, global module ID) is the key and local module ID is the value.'''

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

    return dict(zip(localModuleIDInfo, localModuleIDs))
