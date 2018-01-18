import pandas as pd
import os
path = os.path.abspath('..')
import sys
sys.path.append(path)
import Utilities

waveformName = "Waveforms/waveform.csv"
dataColumns = [(5, "nHitsReturn", "int"), (6, "SSID_readReturn", "int")]

data = pd.read_csv(waveformName)
for (colIndex, colName, colType) in dataColumns:
    values = data[data.columns[colIndex]]
    if (colType == "int"):
        for value in values:
            value = Utilities.binToInt(value)
    else if (colType == "float"):
        for value in values:
            value = Utilities.binToFloat32(value)
