from TTH.MEAnalysis.MEAnalysis_cfg import *
from TTH.MEAnalysis.samples_v1 import lfn_to_pfn, initialize_from_cfgfile
import TTH.MEAnalysis.mem_parameters_cff as mempar
import imp

filename_datacard = os.environ["DATACARD"] + ".py"
imp.load_source("datacard", os.environ["CMSSW_BASE"]+"/src/TTH/MEAnalysis/python/" + filename_datacard)
datacard.configure(process.fwliteInput)

process.fwliteInput.evLimits = cms.vint32([
	int(os.environ["SKIP_EVENTS"]),
	int(os.environ["SKIP_EVENTS"]) + int(os.environ["MAX_EVENTS"])
])

process.fwliteInput.samples = mempar.samples

fns = os.environ["FILE_NAMES"].split()
#if len(fns) != 1:
#	raise Exception("can only process one file at a time")
#fn = fns[0]
dataset = os.environ["DATASETPATH"]

good_samp = []
for ns in range(len(process.fwliteInput.samples)):
	samp = process.fwliteInput.samples[ns]
	if samp.nickName.value() == dataset:
		process.fwliteInput.samples[ns].skip = False
		process.fwliteInput.samples[ns].subFiles = cms.vstring(map(lfn_to_pfn, fns))
		#process.fwliteInput.samples[ns].fullFilename = cms.string(lfn_to_pfn(fn))
		good_samp += [samp]
	else:
		process.fwliteInput.samples[ns].skip = True

process.fwliteInput.samples = good_samp
process.fwliteInput.outFileName = cms.string(os.environ["MY_SCRATCH"] + "/output.root")

if "phys14" in dataset:
    process.fwliteInput.csv_WP_L = 0.423
    process.fwliteInput.csv_WP_M = 0.814
    process.fwliteInput.csv_WP_T = 0.941

print "------"
print process.dumpPython()
print "------"

if __name__ == "__main__":
	of = open("MEAnalysis_cfg.py", "w")
	of.write(process.dumpPython())
	of.close()
