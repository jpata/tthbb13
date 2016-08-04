#!/usr/bin/env python
#This script recursively adds root files in directories
# e.g. /a/b/c/output_*.root -> /a/b/c.root
from TTH.MEAnalysis.ParHadd import par_hadd
import sys, os

infile = sys.argv[1]
lines = open(infile).readlines()
sample_name = lines[0].strip()[1:-1]

print "sample name", sample_name

files = []
for li in lines[1:]:
    fi = li.split()[0]
    if not "root" in fi:
        continue
    files += ["root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat" + fi]
#    files += [fi]
print "files", files

par_hadd("/scratch/" + os.environ["USER"] + "/" + sample_name + ".root", files, 250, 5, 3)
