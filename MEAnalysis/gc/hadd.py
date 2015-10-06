#import TTH.MEAnalysis.JobUtils as ju
from TTH.TTHNtupleAnalyzer.ParHadd import par_hadd
import glob
import sys
import os, fnmatch

ofdir = os.environ.get("HOME") + "/tth/gc/"
samps = []
for x in sys.argv[1:]:
    samps += glob.glob(x + "/*")

for samp in samps:
    if len(samp) == 0:
        continue
    fs = []
    for base, dirs, files in os.walk(samp):
        goodfiles = fnmatch.filter(files, "*.root")
        fs += [os.path.join(base, f) for f in goodfiles]
    fs = glob.glob(samp + "/*.root")
    sampname = samp.split("/")[-1]
    print "merging", samp, sampname, len(fs)
    if len(fs) > 0:
        par_hadd(ofdir + sampname + ".root", fs, 250, 5, 3)
