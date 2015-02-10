from TTH.MEAnalysis.MEAnalysis_cfg import *
import TTH.MEAnalysis.mem_parameters_cff as mempar

process.fwliteInput.evLimits = cms.vint32([
	int(os.environ["SKIP_EVENTS"]),
	int(os.environ["SKIP_EVENTS"]) + int(os.environ["MAX_EVENTS"])
])

process.fwliteInput.samples = mempar.samples

fns = os.environ["FILE_NAMES"].split()
if len(fns) != 1:
	raise Exception("can only process one file at a time!")
	
for ns in range(len(process.fwliteInput.samples)):
	samp = process.fwliteInput.samples[ns]
	if samp.nickName.value() in fns:
		process.fwliteInput.samples[ns].skip = False
	else:
		process.fwliteInput.samples[ns].skip = True


process.fwliteInput.outFileName = cms.string(os.environ["MY_SCRATCH"] + "/output.root")
print "------"
print process.dumpPython()
print "------"