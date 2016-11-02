#!/usr/bin/python
"""
This file contains a few tools to handle sparse histograms.
All tests should be written in test/testDatacards.py
"""
import ROOT

from collections import OrderedDict
import logging

LOG_MODULE_NAME = logging.getLogger(__name__)

def find_axis(h, axname):
    """
    Returns the index of the axis with the given name in the sparse histogram
    h (THNsparse) - the input histogram 
    axname (string) - name of the axis
    returns (int): [0...Naxes] if axis found
    raises:
        KeyError if axis is not found
    """
    iaxis = -1
    axnames = []
    for i in range(h.GetNdimensions()):
        axnames += [h.GetAxis(i).GetName()]
        if h.GetAxis(i).GetName() == axname:
            iaxis = i
            break
    if iaxis == -1:
        raise KeyError("No axis {0} found: axes={1}".format(axname, axnames))
    return iaxis

def set_range(h, axname, loval, hival):
    """
    Configures the sparse histogram to use the specified range on an axis, i.e.
    applies a cut. E.g. "numJets", lo=3, hi=4 sets a cut on 3 < numJets < 4.

    h (THnSparse) - the inout histogram, which is modifed
    axname (string) - name of the axis
    loval (float) - value of the low edge (inclusive)
    hival (float) - value of the high edge (exclusive)
    returns: nothing
    """
    iaxis = find_axis(h, axname)
    lobin = h.GetAxis(iaxis).FindBin(loval)
    hibin = h.GetAxis(iaxis).FindBin(hival) - 1 #this is here to make the upper edge exclusive
    if lobin > hibin:
        LOG_MODULE_NAME.warning("set_range: incorrect ranges: {0} {1}".format(loval, hival))
        hibin = lobin
    LOG_MODULE_NAME.debug("set_range: {0} h.GetAxis({1}).SetRange({2}, {3})".format(axname, iaxis, lobin, hibin))
    h.GetAxis(iaxis).SetRange(lobin, hibin)


def apply_cuts_project(h, cuts, projections):
    """
    Applies a list of cuts and projects out a histogram.
    h (THFn): sparse histogram
    cuts (list of 3-tuples): list of cuts in the form of tuples (variable, loval, hival).
    projections (list): list of variables to project out.
    """
    axs = [find_axis(h, project) for project in projections] + ["E GOFF"]
    LOG_MODULE_NAME.debug("apply_cuts_project: h to axes {1} N={0}".format(
        h.GetEntries(), axs
    ))

    for i in range(h.GetNdimensions()):
        h.GetAxis(i).SetRange(0, h.GetAxis(i).GetNbins() + 1)
        h.GetAxis(i).SetBit(ROOT.TAxis.kAxisRange)

    for c in cuts:
        set_range(h, c[0], c[1], c[2])

    hp = h.Projection(*axs)
    hp.SetDirectory(0)
    hp.SetName("__".join(["__".join(map(str, c)) for c in cuts]) + "__" + "__".join(projections))
    return hp

def mkdirs(fi, path):
    path = path.encode("ascii", "ignore")
    pathspl = path.split("/")
    sfi = fi
    for p in pathspl:
        d = sfi.Get(str(p))
        if d == None:
            d = sfi.mkdir(p)
            d.Write()
        sfi = d
    return sfi


def save_hdict(ofn, hdict):
    """
    Saves a dictionary of ROOT objects in an output file. The objects will be
    renamed according to the keys in the dictionary.

    ofn (string): path to the output file which will be recreated
    hdict (dict): dict of "/absolute/path/objname" -> TObject pairs that will
        be saved to the output.
    returns: nothing
    """
    outfile = ROOT.TFile(ofn, "recreate")
    if not outfile or outfile.IsZombie():
        raise Exception(
            "Could not open output file {0}".format(ofn)
        )
    dirs = {}
    for k, v in sorted(hdict.items(), key=lambda x: x[0]):
        kpath = "/".join(k.split("/")[:-1])
        kname = k.split("/")[-1]
        if len(kname) == 0:
            raise KeyError("Object had no name")
        if kpath:
            try:
                d = outfile.get(kpath)
            except Exception as e:
                d = mkdirs(outfile, kpath)
                dirs[kpath] = d
            assert(v != None)
            v.SetName(kname)
            d.Add(v)
        else:
            v.SetName(kname)
            outfile.Add(v)
    outfile.Write()
    outfile.Close()

def add_hdict(d1, d2):
    """
    Add two sets of dictionaries containing histograms.
    """
    out = OrderedDict()
    ks1 = set(d1.keys())
    ks2 = set(d2.keys())
    for k in ks1.intersection(ks2):
        out[k] = d1[k]
        out[k].Add(d2[k])
        out[k].SetName(d1[k].GetName())
    for k in ks1.difference(ks2):
        out[k] = d1[k]
    for k in ks2.difference(ks1):
        out[k] = d2[k]
    return out
