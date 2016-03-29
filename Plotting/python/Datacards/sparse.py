import rootpy
import rootpy.io
import ROOT
import unittest

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
        out[k] = d1[k].Clone()
        out[k].Add(d2[k])
        out[k].SetName(d1[k].GetName())
    for k in ks1.difference(ks2):
        out[k] = d1[k].Clone()
    for k in ks2.difference(ks1):
        out[k] = d2[k].Clone()
    return out

class SparseToolsTest(unittest.TestCase):
    def setUp(self):
        self.file = ROOT.TFile("/Users/joosep/Documents/tth/data/histograms/ControlPlotsSparse.root")
        self.hsparse = self.file.Get("ttH_hbb/sl/sparse")
    
    def test_find_axis_success(self):
        self.assertEqual(find_axis(self.hsparse, "numJets"), 8)

    def test_find_axis_fail(self):
        def f():
            find_axis(self.hsparse, "asdf")
        self.assertRaises(KeyError, f)

    def test_set_range(self):
        iax = find_axis(self.hsparse, "numJets")

        h1 = self.hsparse.Projection(iax).Clone("p1")

        set_range(self.hsparse, "numJets", 0, 6)
        h2a = self.hsparse.Projection(iax).Clone("p2a")

        set_range(self.hsparse, "numJets", 6, 10)
        h2b = self.hsparse.Projection(iax).Clone("p2b")

        self.assertAlmostEqual(h1.Integral(), h2a.Integral()+h2b.Integral())

    def test_apply_cuts_project_1d(self):
        h1 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        #self.assertIsInstance(h1, rootpy.plotting.hist.Hist)
        self.assertAlmostEqual(h1.Integral(), 48.59897653569705)
        self.assertEqual(h1.GetName(), "numJets__4__6__nBCSVM__1__3__btag_LR_4b_2b_logit")

    def test_apply_cuts_project_2d(self):
        h1 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 100)], ["btag_LR_4b_2b_logit", "common_bdt"])
        #self.assertIs(type(h1), rootpy.plotting.hist.Hist2D)
        self.assertAlmostEqual(h1.Integral(), 61.12569607935839)
        self.assertEqual(h1.GetName(), "numJets__4__6__nBCSVM__1__100__btag_LR_4b_2b_logit__common_bdt")

    def test_save_hdict(self):
        h1 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        h2 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 3, 6)], ["btag_LR_4b_2b_logit"])
        hdict = OrderedDict()
        hdict["ttH_hbb/cat1/blr/hblr"] = h1.Clone("hblr")
        hdict["ttH_hbb/cat2/blr/hblr_asd"] = h2.Clone("hblr_asd")
        save_hdict("test.root", hdict)
        
        inf = rootpy.io.File("test.root")
        h1a = inf.Get("ttH_hbb/cat1/blr/hblr")
        self.assertIsNot(h1a, None)
        self.assertEqual(h1a.Integral(), h1.Integral())

        h2a = inf.Get("ttH_hbb/cat2/blr/hblr_asd")
        self.assertIsNot(h2a, None)
        self.assertEqual(h2a.Integral(), h2.Integral())
        inf.close()

    def test_save_hdict_dupe(self):
        ROOT.TH1F.AddDirectory(False)
        h1 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        h2 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 3, 6)], ["btag_LR_4b_2b_logit"])
        hdict = OrderedDict()
        hdict["data/dl_jge4_tge4/Wmass"] = h1.Clone()
        hdict["data/dl_jge4_tge4/common_bdt"] = h2.Clone()
        save_hdict("test.root", hdict)
        # 
        # inf = rootpy.io.File("test.root")
        # h1a = inf.Get("ttH_hbb/cat1/blr/hblr")
        # self.assertIsNot(h1a, None)
        # self.assertEqual(h1a.Integral(), h1.Integral())
        # 
        # h2a = inf.Get("ttH_hbb/cat1/hblr_asd")
        # self.assertIsNot(h2a, None)
        # self.assertEqual(h2a.Integral(), h2.Integral())
        # inf.close()
    
    def test_save_hdict_many(self):
        ROOT.TH1F.AddDirectory(False)
        h1 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        hdict = OrderedDict()
        for i in range(10000):
            hdict["ttH_hbb/cat{0}/hblr".format(i)] = h1.Clone("h{0}".format(i))
        save_hdict("test.root", hdict)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
