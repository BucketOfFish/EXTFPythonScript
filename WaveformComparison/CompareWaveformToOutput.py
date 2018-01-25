import pandas as pd
import os
path = os.path.abspath('..')
import sys
sys.path.append(path)
import Utilities
import Extrapolator

waveformName = "WaveformComparison/Waveforms/formatt.csv"
dataColumns = [('EXPINSTANCE.EXP/AFW/AUX_SSID_DUDE/exped_ssid_18xN[287:0]', "ssids"), ('EXPINSTANCE.EXP/AFW/sector_Xconstants[287:0]', ""), ('u_ila_1_aux_hit_coordinates[23:0]', ""), ('EXPINSTANCE.EXP/AFW/aux_hit_flag', ""), ('EXPINSTANCE.EXP/AFW/AUX_SSID_DUDE/exped_ssid_18xN__tlast', ""), ('EXPINSTANCE.EXP/AFW/AUX_SSID_DUDE/exped_ssid_18xN_fifo__tvalid', ""), ('EXPINSTANCE.EXP/AFW/sector_Xconstants_valid', "")]

data = pd.read_csv(waveformName)
for rowIndex in range(data.shape[0]):
    row = data.iloc[rowIndex]
    for (colName, colType) in dataColumns:
        value = row[colName]
        if (colType == "int"):
            value = Utilities.binToInt(value)
        else if (colType == "float"):
            value = Utilities.binToFloat32(value)
        else if (colType == "ssids"): # 18 SSIDs, of 16 bits each
            value = Utilities.binToFloat32(value)

extrapolatedGlobalSSIDs = Extrapolator.getExtrapolatedGlobalSSIDs(extrapolatorConstants, inputAUXData, tower, moduleIDDictionary)
AUX coord (phi, eta)\t%d\t%d", aux_hit_coordinates[11:0], aux_hit_coordinates[23:12]")

auxCoords = Utilities.hexToBin(data.iloc[0]['u_ila_1_aux_hit_coordinates[23:0]'])
etaOrSCT = Utilities.binToInt(auxCoords[0:12])
phi = Utilities.binToInt(auxCoords[12:24])
