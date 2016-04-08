#!/usr/bin/python
"""
This file contains a few tools to handle sparse histograms.
All tests should be written in test/testDatacards.py
"""
import rootpy
import rootpy.io
import ROOT

from collections import OrderedDict

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
    for i in range(h.GetNdimensions()):
        if h.GetAxis(i).GetName() == axname:
            iaxis = i
            break
    if iaxis == -1:
        raise KeyError("No axis {0} found".format(axname))
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
    hibin = h.GetAxis(iaxis).FindBin(hival)
    h.GetAxis(iaxis).SetRange(lobin, hibin-1)


def apply_cuts_project(h, cuts, projections):
    """
    Applies a list of cuts and projects out a histogram.
    h (THFn): sparse histogram
    cuts (list of 3-tuples): list of cuts in the form of tuples (variable, loval, hival).
    projections (list): list of variables to project out.
    """
    for i in range(h.GetNdimensions()):
        h.GetAxis(i).SetRange(1, h.GetAxis(i).GetNbins())
    for c in cuts:
        set_range(h, c[0], c[1], c[2])
    axs = [find_axis(h, project) for project in projections]
    hp = h.Projection(*axs).Clone("__".join(["__".join(map(str, c)) for c in cuts]) + "__" + "__".join(projections))
    return rootpy.asrootpy(hp)

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

        try:
            d = outfile.get(kpath)
        except Exception as e:
            d = mkdirs(outfile, kpath)
            dirs[kpath] = d
        assert(v != None)
        v.SetName(kname)
        v.SetDirectory(d)
        #d.Write("", ROOT.TObject.kOverwrite)
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
