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


def save_hdict(ofn, hdict):
    """
    Saves a dictionary of ROOT objects in an output file. The objects will be
    renamed according to the keys in the dictionary.

    ofn (string): path to the output file which will be recreated
    hdict (dict): dict of "/absolute/path/objname" -> TObject pairs that will
        be saved to the output.
    returns: nothing
    """
    outfile = rootpy.io.File(ofn, "recreate")

    for k, v in hdict.items():
        kpath = "/".join(k.split("/")[:-1])
        kname = k.split("/")[-1]
        if len(kname) == 0:
            raise KeyError("Object had no name")

        try:
            d = outfile.get(kpath)
        except rootpy.io.file.DoesNotExist as e:
            d = outfile.mkdir(kpath, recurse=True)

        v.SetName(kname)
        v.SetDirectory(d)
        d.Write("", ROOT.TObject.kOverwrite)
    outfile.Close()

class InputKey(object):
    def __init__(self, sample, systematic):
        self.sample = sample
        self.systematic = systematic

class OutputRenameRule(object):
    """
    Base class for renaming output histograms based on
    the sample name and rule.
    E.g. you can do
    SingleMuon/numJets__6__8__nBCSVM__4__8/mem_SL_0w2h2t -> data/6j4t/mem
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, sample_name, rule):
        return self.func(sample_name, rule)

class SampleFilter(object):
    """
    A base class for a filter applied on a rule.
    The filter works on the basis of the sample names and returns
    a boolean if the rule is to be applied on this sample.
    """
    def __init__(self):
        pass

    def __call__(self, sample_name):
        return True

class DataFilter(SampleFilter):
    """
    A Filter that can be configured to accept only the dataset
    that corresponds to the particular analysis channel.
    This is needed in order to not add together SingleMuon and SingleElectron
    events in an incorrect and overlapping way
    """

    def __init__(self, dname):
        """
        dname (string): name of the channel. Should be one of "mu", "el"
        """
        self.dname = dname

    def __call__(self, sn):
        if "Single" in sn.sample:
            if self.dname == "mu":
                return sn.sample == "SingleMuon"
            elif self.dname == "el":
                return sn.sample == "SingleElectron"
        if "Double" in sn.sample or "MuonEG" in sn.sample:
            return False
        return True

class RenameRule(OutputRenameRule):
    """
    Renames the output histogram according to the sample and Rule which produced
    it.
    """
    def __init__(self):
        pass

    def __call__(self, key, rule, histname):
        """
        key (InputKey): represents the origin of the input THn
        rule (Rule): the Rule that created the histogram that being renamed
        histname (string): name of the output distribution, e.g. "mem"

        returns (string): full path of the histogram in the output file
        """
        sample = key.sample
        systematic = key.systematic
        return "{0}/{1}/{2}/{3}".format(sample, rule.name, rule.project_axes_str(), histname)

class DataRenameRule(RenameRule):
    """
    Rule to rename histograms derived from data.
    """
    def __init__(self, parent_rule):
        self.parent_rule = parent_rule
        super(DataRenameRule, self).__init__()

    def __call__(self, key, rule, histname):
        """
        Overrides the sample name from e.g. SingleMuon to data
        Parameters as ``RenameRule.__call__``
        """
        if key.sample in ["SingleMuon", "SingleElectron", "DoubleMuon", "DoubleEG", "MuonEG"]:
            key = InputKey("data", "nominal")
        return super(DataRenameRule, self).__call__(key, self.parent_rule, histname)

class ProjectionRule(object):
    """
    Specifies how a projection is made from a sparse histogram.
    The sparse histogram can have string qualifiers specifying the process
    and systematic scenario.

    The projection is defined by a list of cuts, which are currently 3-tuples
    with (axisname, lovalue, hivalue).

    The rule can selectively process samples by applying a ``SampleFilter``,
    which decides based on the name of the sample if this rule should
    be applied.
    
    The output of applying the rule on a collection (OrderedDict) of sparse histograms
    is a TH1D, which can be selectively renamed based on a ``RenameRule``
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.cuts = kwargs.get("cuts")
        self.project_axes = kwargs.get("project_axes")
        self.sample_filter = kwargs.get("sample_filter", SampleFilter())
        self.output_rename = kwargs.get("output_rename", RenameRule())
        self.rebin = kwargs.get("rebin", 1)

    def __call__(self, input):
        out = OrderedDict()
        for (inputkey, hist) in input.items():
            if not self.sample_filter(inputkey):
                continue
            ret = apply_cuts_project(hist, self.cuts, self.project_axes)
            ret.Rebin(self.rebin)

            if inputkey.systematic == "nominal":
                ret.SetName(self.project_axes_str())
            else:
                ret.SetName(self.project_axes_str() + "_" + inputkey.systematic)
            out[self.output_rename(inputkey, self, ret.GetName())] = ret
        return out

    def cut_str(self):
        """
        String representation of the cuts.
        """
        return "__".join(["__".join([str(y) for y in x]) for x in self.cuts])

    def project_axes_str(self):
        """
        String representation of the axes that are projected.
        """
        return "__".join(self.project_axes)

def add_hdict(d1, d2):
    """
    Add two sets of dictionaries containing histograms.
    """
    out = OrderedDict()
    ks1 = set(d1.keys())
    ks2 = set(d2.keys())
    for k in ks1.intersection(ks2):
        out[k] = d1[k] + d2[k]
        out[k].SetName(d1[k].GetName())
    for k in ks1.difference(ks2):
        out[k] = d1[k].Clone()
    for k in ks2.difference(ks1):
        out[k] = d2[k].Clone()
    return out

def apply_rules(input, rules):
    """
    Applies a list of rules on an input.

    input (OrderedDict): a dictionary of 
    """
    out = OrderedDict()
    rules_out = []
    for rule_name, rule in rules.items():
        rule_out = rule(input)
        rules_out += [rule_out]
    out = reduce(add_hdict, rules_out)
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
        self.assertIsInstance(h1, rootpy.plotting.hist.Hist)
        self.assertAlmostEqual(h1.Integral(), 98.07965384168327)
        self.assertEqual(h1.GetName(), "numJets__4__6__nBCSVM__1__3__btag_LR_4b_2b_logit")

    def test_apply_cuts_project_1d(self):
        h1 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 100)], ["btag_LR_4b_2b_logit", "common_bdt"])
        #self.assertIs(type(h1), rootpy.plotting.hist.Hist2D)
        self.assertAlmostEqual(h1.Integral(), 123.3783247201219)
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
        h1 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        h2 = apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 3, 6)], ["btag_LR_4b_2b_logit"])
        hdict = OrderedDict()
        hdict["ttH_hbb/cat1/blr/hblr"] = h1.Clone()
        hdict["ttH_hbb/cat1/hblr_asd"] = h2.Clone()
        save_hdict("test.root", hdict)
        
        inf = rootpy.io.File("test.root")
        h1a = inf.Get("ttH_hbb/cat1/blr/hblr")
        self.assertIsNot(h1a, None)
        self.assertEqual(h1a.Integral(), h1.Integral())

        h2a = inf.Get("ttH_hbb/cat1/hblr_asd")
        self.assertIsNot(h2a, None)
        self.assertEqual(h2a.Integral(), h2.Integral())
        inf.close()


class RuleTest(unittest.TestCase):

    def test_InputKey(self):
        ik = InputKey("ttH_hbb", "nominal")
        self.assertEquals(ik.sample, "ttH_hbb")
        self.assertEquals(ik.systematic, "nominal")

    def test_DataFilter(self):
        df = DataFilter("mu")
        for d in ["ttH_hbb", "SingleMuon"]:
            self.assertEquals(df(InputKey(d, "nominal")), True)
        for d in ["SingleElectron", "DoubleMuon", "DoubleEG", "MuonEG"]:
            self.assertEquals(df(InputKey(d, "nominal")), False)

        df = DataFilter("el")
        for d in ["ttH_hbb", "SingleElectron"]:
            self.assertEquals(df(InputKey(d, "nominal")), True)
        for d in ["SingleMuon", "DoubleMuon", "DoubleEG", "MuonEG"]:
            self.assertEquals(df(InputKey(d, "nominal")), False)

    def test_RenameRule(self):
        rn = RenameRule()
        r = ProjectionRule(
            name="6j4t",
            cuts = [("numJets", 6, 8), ("nBCSVM", 4, 8)],
            project_axes=["mem_SL_0w2h2t"],
        )

        out = rn(
            InputKey("ttH_hbb", "nominal"),
            r,
            "mem_SL_0w2h2t"
        )
        self.assertEquals(out, "ttH_hbb/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t")

        #FIXME
        #the renaming of the histogram object is done only by the ProjectionRule that makes the histogram,
        #not the actual RenameRule, which only produces a string
        out = rn(
            InputKey("ttH_hbb", "CMS_JESUp"),
            r,
            "mem_SL_0w2h2t"
        )
        self.assertEquals(out, "ttH_hbb/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t")
        #self.assertEquals(out, "ttH_hbb/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t_CMS_JESUp")

    def test_DataRenameRule(self):

        r = ProjectionRule(
            name="6j4t",
            cuts = [("numJets", 6, 8), ("nBCSVM", 4, 8)],
            project_axes=["mem_SL_0w2h2t"],
        )
        rn = DataRenameRule(r)

        out = rn(
            InputKey("ttH_hbb", "nominal"),
            r,
            "mem_SL_0w2h2t"
        )
        self.assertEquals(out, "ttH_hbb/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t")

        out = rn(
            InputKey("SingleMuon", "nominal"),
            r,
            "mem_SL_0w2h2t"
        )
        self.assertEquals(out, "data/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t")


    def test_ProjectionRule(self):

        file = ROOT.TFile("/Users/joosep/Documents/tth/data/histograms/ControlPlotsSparse.root")
        hsparse_sig = file.Get("ttH_hbb/sl/sparse")
        hsparse_sig_jUp = file.Get("ttH_hbb/sl/sparse_CMS_scale_jUp")
        hsparse_bkg = file.Get("ttbarOther/sl/sparse")
        hsparse_data = file.Get("SingleMuon/sl/sparse")
    
        r = ProjectionRule(
            name="6j4t",
            cuts = [("numJets", 6, 8), ("nBCSVM", 4, 8)],
            project_axes=["mem_SL_0w2h2t"],
        )
        r.output_rename = DataRenameRule(r)

        input = OrderedDict()
        input[InputKey("ttH_hbb", "nominal")] = hsparse_sig
        input[InputKey("ttH_hbb", "CMS_scale_jUp")] = hsparse_sig_jUp
        input[InputKey("ttbarOther", "nominal")] = hsparse_bkg
        input[InputKey("SingleMuon", "nominal")] = hsparse_data
        
        ret = r(input)
        print ret
        self.assertIn("ttH_hbb/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t", ret.keys())
        h = ret["ttH_hbb/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t"]
        self.assertAlmostEquals(h.Integral(), 6.3561650237769225)

        self.assertIn("ttH_hbb/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t_CMS_scale_jUp", ret.keys())
        h = ret["ttH_hbb/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t_CMS_scale_jUp"]
        self.assertAlmostEquals(h.Integral(), 6.68035408513626)

        self.assertIn("data/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t", ret.keys())
        h = ret["data/6j4t/mem_SL_0w2h2t/mem_SL_0w2h2t"]
        self.assertAlmostEquals(h.Integral(), 5.0)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
