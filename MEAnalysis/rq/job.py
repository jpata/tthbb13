
import matplotlib
from matplotlib import rc
#temporarily disable true latex for fast testing
rc('text', usetex=False)
matplotlib.use('PS') #needed on T3
import matplotlib.pyplot as plt


import ROOT
import TTH.MEAnalysis.counts as counts
import TTH.Plotting.joosep.sparsinator as sparsinator
import tempfile, os
from shutil import copyfile

import sys, os, copy
from collections import OrderedDict
import TTH.Plotting.joosep.plotlib as plotlib #heplot, 


import rootpy
from rootpy.plotting import Hist
from rootpy.plotting import root2matplotlib as rplt

from TTH.Plotting.joosep import controlPlot

from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

def copy_rsync(src, dst):
    os.system("rsync --bwlimit=20000 {0} {1}".format(src, dst))

def count(filenames):
    ofname = tempfile.mktemp() 
    ret = counts.main(filenames, ofname)
    os.remove(ofname)
    return ret

def sparse(config_path, filenames, sample, outfile):
    an_name, analysis = analysisFromConfig(config_path)
    temppath = os.path.join("/scratch/{0}/".format(os.environ["USER"]))
    if not os.path.isdir(temppath): 
        os.makedirs(temppath)
    ofname = tempfile.mktemp(dir=temppath)
    sparsinator.main(analysis, filenames, sample, ofname)

    basepath = os.path.dirname(outfile)
    if not os.path.isdir(basepath):
        os.makedirs(basepath)

    copy_rsync(ofname, outfile)
    os.remove(ofname)
    return outfile

#def plot_syst_updown(nominal, up, down):
#    plt.figure(figsize=(6,6))
#    heplot.barhist(nominal, color="black")
#    heplot.barhist(up, color="red")
#    heplot.barhist(down, color="blue")




def plot(kwargs):
    return controlPlot.plot_worker(kwargs)
