#import TTH.MEAnalysis.JobUtils as ju
from TTH.TTHNtupleAnalyzer.ParHadd import par_hadd
import glob
import sys

samps = []
for x in sys.argv[1:]:
    samps += glob.glob(x + "/*")

for samp in samps:
    if len(samp) == 0:
        continue
    fs = glob.glob(samp + "/*.root")
    if len(fs) > 0:
        par_hadd(samp + ".root", fs, 250, 5, 3)
