
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
import glob

import sys, os, copy
from collections import OrderedDict
import TTH.Plotting.joosep.plotlib as plotlib #heplot, 
import subprocess

import rootpy
from rootpy.plotting import Hist
from rootpy.plotting import root2matplotlib as rplt

from TTH.Plotting.joosep import controlPlot

from TTH.Plotting.Datacards.AnalysisSpecificationClasses import Analysis
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
    analysis = Analysis.deserialize(config_path)

    temppath = os.path.join("/scratch/{0}/".format(os.environ["USER"]))
    
    #output path may already be created by other jobs, so just assume it's there
    try:
        os.makedirs(temppath)
    except OSError as e:
        print e
    #create a temporary file name
    
    ofname = tempfile.mktemp(dir=temppath)
    sparsinator.main(analysis, filenames, sample, ofname)

    basepath = os.path.dirname(outfile)
    try:
        os.makedirs(basepath)
    except OSError as e:
        print e

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
        cmd = ["hadd", "-f", outfile] + infiles
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        out, err = process.communicate()
        retcode = process.returncode
        if retcode != 0:
            raise Exception("Could not merge: {0}".format(err))
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
    f = filter(
        lambda x: x.endswith(".root"),
        glob.glob("/mnt/t3nfs01/data01/shome/jpata/tth/sw/CMSSW/src/TTH/MEAnalysis/rq/results/ff7b3731-b583-42e0-961e-66f90d261cc1/sparse/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/*.root")
    )
    mergeFiles(
        "./sparse2.root",
        f    
    )
