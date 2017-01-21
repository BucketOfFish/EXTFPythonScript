inputAUXData_FileName = 'Data/VivianaFTKInputFiles/testvectors/aux_stream32_01.dat' # AUX input data
shiftBitAUX = True # move the last hex character of each line to the front (a formatting issue)
inputDFData_FileName = 'Data/VivianaFTKInputFiles/testvectors/df_stream32_01.dat' # DF data
shiftBitDF = True # move the last hex character of each line to the front (a formatting issue)

moduleIDDictionary_FileName = 'Data/raw_12LiblHW_32.moduleidmap' # maps between local module ID, tower, layer, and gloabl module ID

extrapolatorConstants_FileName = 'Data/VivianaFTKInputFiles/constants/EXPConstants_reg22.txt' # matrix and vector constants for ex.
TFConstants_FileName = 'Data/VivianaFTKInputFiles/constants/TFConstants_reg22.txt' # matrix and vector constants for track fitter

tower = 22 # what tower the hits are on
