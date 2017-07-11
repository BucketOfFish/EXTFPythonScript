inputAUXData_FileName = 'Data/tvec_AUX_tower11_2P40T.txt' # AUX input data
shiftBitAUX = False # move the last hex character of each line to the front (a formatting issue)
inputDFData_FileName = 'Data/testvector_DF11_2event.dat' # DF data
shiftBitDF = False # move the last hex character of each line to the front (a formatting issue)

moduleIDDictionary_FileName = 'Data/raw_12LiblHW_32.moduleidmap' # maps between local module ID, tower, layer, and gloabl module ID

extrapolatorConstants_FileName = 'Data/EXP_T11_21P.txt' # matrix and vector constants for extrapolator
TFConstants_FileName = 'Data/TFConstants_15sector.txt' # matrix and vector constants for track fitter

tower = 11 # what tower the hits are on
