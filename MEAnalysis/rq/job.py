import ROOT

def myjob(filename):
    print "myjob: filename={0}".format(filename)
    fi = ROOT.TFile.Open("root://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat" + filename)
    tree = fi.Get("tree")

    h = ROOT.TH1D("", "", 100, 0, 500)
    h.SetDirectory(0)
    for iev in range(tree.GetEntries()):
        tree.GetEntry(iev)
        h.Fill(tree.jets_pt[0])
        if iev>1000:
            break
    return h

if __name__ == "__main__":
    myjob()
