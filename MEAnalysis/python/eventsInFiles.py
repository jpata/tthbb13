import ROOT
import sys
import subprocess
import re

treename = sys.argv[1]
prefix = sys.argv[2]
indata = sys.argv[3:]
files = []

for line in indata:
    fi = line.split()[0]
    if fi.endswith("root"):
        files += [prefix + fi.strip()]

for infile in files:
    tf = ROOT.TFile.Open(infile)
    tt = tf.Get(treename)
    events = tt.GetEntries()
    tf.Close()
    print "{0} = {1}".format(infile, events)
