inputAUXData_FileName = 'Data/Jon4Track/test_vector_aux_ftksim_1.dat' # AUX input data
shiftBitAUX = True # move the last hex character of each line to the front (a formatting issue)
inputDFData_FileName = 'Data/Jon4Track/test_vector_df_ftksim_1.dat' # DF data
shiftBitDF = True # move the last hex character of each line to the front (a formatting issue)

moduleIDDictionary_FileName = 'Data/raw_12LiblHW_32.moduleidmap' # maps between local module ID, tower, layer, and gloabl module ID

extrapolatorConstants_FileName = 'Data/EXPConstants_tower22.txt' # matrix and vector constants for extrapolator
TFConstants_FileName = 'Data/TFConstants_reg22.txt' # matrix and vector constants for track fitter

tower = 22 # what tower the hits are on
