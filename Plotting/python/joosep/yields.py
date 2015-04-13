import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os
import numpy as np

categories = dict([
    ("cat1", "(cat==1)"),
    ("cat2", "(cat==2)"),
    ("cat3", "(cat==3)"),
    ("cat6", "(cat==6)"),
])

categories_btag = dict([
    ("L", "(cat_btag==0)"),
    ("H", "(cat_btag==1)"),
])

lep_reco_cats = dict([
    ("sl", "(nleps==1)"),
    ("dl", "(nleps==2)"),
])

jet_cats = dict([
    ("4j", "(njets==4)"),
    ("5j", "(njets==5)"),
    ("6j", "(njets==6)"),
    ("7j+", "(njets>6)"),
])

btag_cats = dict([
    ("0t", "(nBCSVM==0)"),
    ("1t", "(nBCSVM==1)"),
    ("2t", "(nBCSVM==2)"),
    ("3t", "(nBCSVM==3)"),
    ("4t", "(nBCSVM==4)"),
    ("5t+", "(nBCSVM>4)"),
])

def get_entries(tree, cut, normalize=False):
    if normalize:
        I = tree.GetEntries()
    else:
        I = 1.0
    return float(tree.GetEntries(cut) / I)

def yields_cat(filename):
    tf = ROOT.TFile(filename)
    tree = tf.Get("tree")

    row = np.zeros((1, 18))
    row[0, 0:6] = [
        get_entries(tree, lep_reco_cats["sl"] + "&&" + jet_cats["4j"] + "&&" + btag_cats[x])
        for x in sorted(btag_cats.keys())
    ]
    row[0, 6:12] = [
        get_entries(tree, lep_reco_cats["sl"] + "&&" + jet_cats["5j"] + "&&" + btag_cats[x])
        for x in sorted(btag_cats.keys())
    ]
    row[0, 12:18] = [
        get_entries(tree, lep_reco_cats["sl"] + "&&" + jet_cats["6j"] + "&&" + btag_cats[x])
        for x in sorted(btag_cats.keys())
    ]
    print "      |" + "\t|".join(sorted(btag_cats.keys()))
    print "SL 4J |", "\t|".join(map(lambda x: "%.0f"%x, row[0, 0:6]))
    print "SL 5J |", "\t|".join(map(lambda x: "%.0f"%x, row[0, 6:12]))
    print "SL 6J |", "\t|".join(map(lambda x: "%.0f"%x, row[0, 12:18]))
    return row
if __name__ == "__main__":
    yields_cat(sys.argv[1])
