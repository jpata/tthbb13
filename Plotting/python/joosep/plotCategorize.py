import sys
import matplotlib
matplotlib.use('Agg')
sys.path += ["/Users/joosep/Documents/heplot/"]
import heplot, rootpy
import numpy as np
import matplotlib.pyplot as plt
import pandas
import rootpy.plotting.root2matplotlib as rplt
import ROOT, plotlib, heplot
import tabulate
import cPickle as pickle
from collections import OrderedDict

#Categorizer
sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/Datacards/")
import Categorize, Forest, TreeAnalysis
import Cut

def integral_and_error(h):
    e = ROOT.Double()
    i = h.IntegralAndError(1, h.GetNbinsX(), e)
    return i, e

backgrounds = ["ttbarOther", "ttbarPlusBBbar", "ttbarPlusB", "ttbarPlus2B", "ttbarPlusCCbar"]

slist = [
 ('ttH_hbb', 'ttHbb'),
 ('ttbarPlusBBbar', 'ttbarPlusBBbar'),
 ('ttbarPlusB', 'ttbarPlusB'),
 ('ttbarPlus2B', 'ttbarPlus2B'),
 ('ttbarPlusCCbar', 'ttbarPlusCCbar'),
 ('ttbarOther', 'ttbarOther')
]

systematics=[
    ("_CMS_scale_jUp", "_CMS_scale_jDown"),
    ("_CMS_ttH_CSVLFUp", "_CMS_ttH_CSVLFDown"),
    ("_CMS_ttH_CSVHFUp", "_CMS_ttH_CSVHFDown"),
    ("_CMS_ttH_CSVStats1Up", "_CMS_ttH_CSVStats1Down"),
    ("_CMS_ttH_CSVStats2Up", "_CMS_ttH_CSVStats2Down"),
]

path_to_data = "/Users/joosep/Dropbox/tth"
categorization = "old"

def plotCategoryLimit(pickle_fn, catname, takeLeaves=False):
    """
    takeLeaves -
        True: limit plot will be done only with the leaves of the categorization tree (e.g. blr split)
        False: limit plot will be done with the nodes one leaf up from the categorization tree (e.g. blr unsplit) 
    """
    categories_pi_file = open(pickle_fn)
    categories = pickle.load(categories_pi_file)
    categories_pi_file.close()

    #find the leaves and nodes corresponding to the Categorization
    leaves = []
    nodes = []
    Categorize.Recurse(categories, 0, leaves, nodes)

    
    lims = []
    ks = []
    knames = []
    i = 0
    for n in nodes:

        #skip nodes which are to be ignored
        if n.discriminator_axis is None:
            continue
        if takeLeaves:
            #is not a leaf
            if len(n.children) != 0 and "Whole" not in str(n):
                continue
        else:
            if len(n.children) == 0:
                continue
            if not (n.depth == 0 or (len(n.children[0].children) + len(n.children[1].children)) == 0):
                continue

        #median limit
        l = n.limits_comb[0][2]
        print "accept", str(n), l

        lims += [n.limits_comb]
        ks += [i]

        #rename the total limit
        if  "Whole" in str(n):
            knames += ["combined"]
        else:
            knames += [n.latex_string()]
        i += 1

    fig = plt.figure(figsize=(10,int(len(lims)*0.6)))
    plotlib.brazilplot(lims, ks[::-1], knames[::-1])
    plt.xscale("log")
    plt.xlim(1.0, max([l[0][2] for l in lims])*5)
    suffix = ""
    if takeLeaves:
        suffix += "leaves"
    plotlib.svfg("plots/limits_{0}{1}.png".format(catname, suffix))
    plt.clf()
    del fig

def plotCategoryLeaves(pickle_fn, root_fn, catname):

    categories_pi_file = open(pickle_fn)
    categories = pickle.load(categories_pi_file)
    categories_pi_file.close()

    #find the leaves and nodes corresponding to the Categorization
    leaves = []
    nodes = []
    Categorize.Recurse(categories, 0, leaves, nodes)

    categories_root_file = rootpy.io.File(root_fn)

    for leaf in leaves:
        if str(leaf.discriminator_axis) == "counting" or leaf.discriminator_axis is None:
            continue
        for proc in [s[0] for s in slist]:
            for systUp, systDown in systematics:
                fig = plt.figure()
                syst = systUp.replace("Up", "")
                h0 = categories_root_file.Get("{0}/{1}/{2}{3}".format(proc, str(leaf), str(leaf.discriminator_axis), systUp))
                h1 = categories_root_file.Get("{0}/{1}/{2}{3}".format(proc, str(leaf), str(leaf.discriminator_axis), systDown))
                h = categories_root_file.Get("{0}/{1}/{2}".format(proc, str(leaf), str(leaf.discriminator_axis)))
                heplot.barhist(h0, color="blue", label="up $N={0:.1f} \pm {1:.1f}$".format(*integral_and_error(h0)))
                heplot.barhist(h1, color="red", label="down $N={0:.1f} \pm {1:.1f}$".format(*integral_and_error(h1)))
                heplot.barhist(h, color="black", label="central $N={0:.1f} \pm {1:.1f}$".format(*integral_and_error(h)), lw=2)
                plt.title(proc.replace("_", " ") + " " + leaf.latex_string() + " " + syst.replace("_", " "))
                plt.legend(loc="best")
                fn = "plots/{0}_{1}_{2}.png".format(proc, str(leaf), syst)
                plotlib.svfg(fn)
                plt.clf()
                del fig

if __name__ == "__main__":
    pi_file = "{0}/{1}.pickle".format(path_to_data, categorization)
    root_file = pi_file.replace("pickle", "root")
    plotCategoryLimit(pi_file, categorization, takeLeaves=True)
    plotCategoryLeaves(pi_file, root_file, categorization)
