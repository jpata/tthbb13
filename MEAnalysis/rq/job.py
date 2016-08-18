import ROOT
import TTH.MEAnalysis.counts as counts
import tempfile, os

def count(filenames):
    ofname = tempfile.mktemp() 
    ret = counts.main(filenames, ofname)
    os.remove(ofname)
    return ret
