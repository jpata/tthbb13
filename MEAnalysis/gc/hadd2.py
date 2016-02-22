#!/usr/bin/env python
#This script recursively adds root files in directories
# e.g. /a/b/c/output_*.root -> /a/b/c.root
from TTH.TTHNtupleAnalyzer.ParHadd import par_hadd
import glob
import sys
import os, fnmatch

all_rootfiles = []

#recurse over the given path
for path, dirs, files in os.walk(sys.argv[1]):
    #Check if there are root files in this path
    rootfiles = filter(lambda x: x.endswith("root"), files)
    #Add the full path
    rootfiles = map(lambda f: os.path.join(path, f), rootfiles)
    all_rootfiles += rootfiles

sample_name = sys.argv[1].strip("/").split("/")[-1]
par_hadd("/scratch/" + os.environ["USER"] + "/" + sample_name + ".root", all_rootfiles, 250, 5, 3)
