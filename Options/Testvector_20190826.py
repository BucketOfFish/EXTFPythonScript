# Comparing against testvector output.
# Email from Jon:
#
# Hi Matt,
#
# I have a good test case for your SSB simulation script.  We have spybuffers in the solorun output here: https://its.cern.ch/jira/browse/FTKHWD-1210 
# /eos/atlas/atlascerngroupdisk/det-ftk/SoloRun/2019-08-19/12h52m33s/FTK_SliceA/SSB/crate-4/slot-6/ssb_spybuffer_dump_main_FPGA0.dat
#
# Could you grab an event and feed it into your script? It's for tower22.  It's supposed to be the same event repeated, so to start off with the first whole event should work.  If you can give me the expected output packet I can compare it with the output spybuffer.   
#
# Second, as a consistency check, it would be interesting to see if what you get matches FTKSim.  This directory has input and output testvectors: /eos/atlas/atlascerngroupdisk/det-ftk/tvlibrary/data18_pp_2017HighDF128/Tower_6_22_128_358333_lb70_ev140/SSB_22 
# inputAUXA.txt  inputAUXB.txt  output_ssb_tower22.dat are the AUX A/B and DF inputs.  Can you run these and then we we can compare it with the expected output from FTKSim output.txt
#
# Thanks,
# Jonathan

# up-to-date inputs as of 2019-08-09
# inputAUXData_FileName = 'Data/Testvector_20190826/inputAUXA.txt' # AUX input data
inputAUXData_FileName = 'Data/Testvector_20190826/inputAUXB.txt' # AUX input data
shiftBitAUX = False # move the last hex character of each line to the front (a formatting issue)
inputDFData_FileName = 'Data/Testvector_20190826/output_ssb_tower22.dat' # DF data
shiftBitDF = False # move the last hex character of each line to the front (a formatting issue)

# both Libl3D and LiblHW tested compatible as of 2019-08-09 - not sure which one to use
moduleIDDictionary_FileName = 'Data/raw_12Libl3D.moduleidmap' # maps between local module ID, tower, layer, and gloabl module ID

# up-to-date constants as of 2019-08-09
extrapolatorConstants_FileName = 'Data/EXPConstants_reg22_IBL_hw_scale_10.2.txt' # matrix and vector constants for extrapolator
TFConstants_FileName = 'Data/TFConstants_reg22_IBL_hw_scale_10.2.txt' # matrix and vector constants for track fitter

tower = 22 # what tower the hits are on
