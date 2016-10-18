
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
import shutil
from shutil import copyfile

import sys, os, copy
from collections import OrderedDict
import TTH.Plotting.joosep.plotlib as plotlib #heplot, 


import rootpy
from rootpy.plotting import Hist
from rootpy.plotting import root2matplotlib as rplt

from TTH.Plotting.joosep import controlPlot

from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig
from TTH.Plotting.Datacards import MakeCategory
from TTH.Plotting.Datacards import MakeLimits

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


def mergeFiles(outfile, infiles, remove_inputs=False):
    basepath = os.path.dirname(outfile)
    if not os.path.isdir(basepath):
        os.makedirs(basepath)

    if len(infiles) == 1:
        shutil.copy(infiles[0], outfile)
    else:
        merger = ROOT.TFileMerger(False)
        merger.OutputFile(outfile)
        for res in infiles:
            merger.AddFile(res, False)
        merger.Merge()
    if remove_inputs:
        for res in infiles:
            if os.path.isfile(res):
                os.remove(res)
    return outfile

def makecategory(*args):
    an_name, analysis = analysisFromConfig(args[0])
    new_args = [analysis] + list(args)[1:]
    new_args = tuple(new_args)
    return MakeCategory.main(*new_args)

def plot(*kwargs):
    return controlPlot.plot_worker(*kwargs)

def makelimits(*args):
    #an_name, analysis = analysisFromConfig(args[1])
    return MakeLimits.main(*args)

if __name__ == "__main__":
    sparse(
        'results/29d43491-3535-4ab2-9c34-85ae14cc2e91/analysis.cfg', ['root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/tth/Sep29_v1/TT_TuneCUETP8M1_13TeV-powheg-pythia8/Sep29_v1/160930_165709/0000/tree_1.root', 'root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/tth/Sep29_v1/TT_TuneCUETP8M1_13TeV-powheg-pythia8/Sep29_v1/160930_165709/0000/tree_10.root'], 'TT_TuneCUETP8M1_13TeV-powheg-pythia8',
        'results/29d43491-3535-4ab2-9c34-85ae14cc2e91/sparse/TT_TuneCUETP8M1_13TeV-powheg-pythia8/sparse_0.root'
    )
