# up-to-date inputs as of 2019-08-09
inputAUXData_FileName = 'Data/jon_nov29_aux.txt' # AUX input data
shiftBitAUX = False # move the last hex character of each line to the front (a formatting issue)
inputDFData_FileName = 'Data/jon_nov29_df.txt' # DF data
shiftBitDF = False # move the last hex character of each line to the front (a formatting issue)

# both Libl3D and LiblHW tested compatible as of 2019-08-09 - not sure which one to use
moduleIDDictionary_FileName = 'Data/raw_12Libl3D.moduleidmap' # maps between local module ID, tower, layer, and gloabl module ID

# up-to-date constants as of 2019-08-09
extrapolatorConstants_FileName = 'Data/EXPConstants_reg22_IBL_hw_scale_10.2.txt' # matrix and vector constants for extrapolator
TFConstants_FileName = 'Data/TFConstants_reg22_IBL_hw_scale_10.2.txt' # matrix and vector constants for track fitter

tower = 22 # what tower the hits are on
