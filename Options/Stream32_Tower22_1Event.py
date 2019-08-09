inputAUXData_FileName = 'Data/aux_stream32_tower22_1event.dat' # AUX input data
shiftBitAUX = False # move the last hex character of each line to the front (a formatting issue)
inputDFData_FileName = 'Data/df_stream32_tower22_1event.dat' # DF data
shiftBitDF = False # move the last hex character of each line to the front (a formatting issue)

# moduleIDDictionary_FileName = 'Data/raw_12Libl3D.moduleidmap' # maps between local module ID, tower, layer, and gloabl module ID # correct one for AUX/EXP
moduleIDDictionary_FileName = 'Data/raw_12LiblHW_32.moduleidmap' # maps between local module ID, tower, layer, and gloabl module ID # correct one for DF

extrapolatorConstants_FileName = 'Data/EXPConstants_tower22.txt' # matrix and vector constants for extrapolator
TFConstants_FileName = 'Data/TFConstants_15sector.txt' # matrix and vector constants for track fitter

tower = 22 # what tower the hits are on
