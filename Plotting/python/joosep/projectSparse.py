import ROOT
from rootpy.plotting import root2matplotlib as rplt

import sys
sys.path += ["/Users/joosep/Documents/heplot"]
import heplot

sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/joosep/")
sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/Datacards/")
import sparse
import plotlib

from plotlib import *
from rootpy.plotting import Hist
import Categorize, Cut

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
    def __init__(self, func):
        self.func = func

    def __call__(self, sample_name):
        return self.func(sample_name)

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
        if key.sample in ["SingleMuon", "SingleElectron"]:
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
        self.sample_filter = kwargs.get("sample_filter")
        self.output_rename = kwargs.get("output_rename")
        self.rebin = kwargs.get("rebin", 1)

    def __call__(self, input, rule_name):
        out = OrderedDict()
        for (inputkey, hist) in input.items():
            if not self.sample_filter(inputkey):
                continue
            ret = sparse.apply_cuts_project(hist, self.cuts, self.project_axes)
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

def makeRule_SL(rules):
    outrules = OrderedDict()
    for rulename, rule in rules.items():
        outrules[rulename + "_mu"] = ProjectionRule(
            name=rule.name,
            cuts=rule.cuts + [("leptonFlavour", 1, 2)],
            project_axes=rule.project_axes,
            sample_filter=DataFilter("mu"),
            output_rename=DataRenameRule(rule),
            rebin=rule.rebin
        )
        outrules[rulename + "_el"] = ProjectionRule(
            name=rule.name,
            cuts=rule.cuts + [("leptonFlavour", 2, 3)],
            project_axes=rule.project_axes,
            sample_filter=DataFilter("el"),
            output_rename=DataRenameRule(rule),
            rebin=rule.rebin
        )
    return outrules

def add_hdict(d1, d2):
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
        rule_out = rule(input, rule_name)
        rules_out += [rule_out]
    out = reduce(add_hdict, rules_out)
    return out

if __name__ == "__main__":

    hsparse = Categorize.GetSparseHistograms(
        "/Users/joosep/Documents/tth/data/histograms/ControlPlotsSparse.root",
        ["ttH_hbb"],
        [
            "ttbarPlus2B",
            "ttbarPlusB",
            "ttbarPlusBBbar",
            "ttbarPlusCCbar",
            "ttbarOther"
        ],
        category="sl",
        data=["SingleMuon", "SingleElectron"]
    )
    rules_bdt = OrderedDict()
    rules_mem = OrderedDict()

    cuts = [
        ("6j4t", [("numJets", 6, 8), ("nBCSVM", 4, 8)]),
        ("6j3t", [("numJets", 6, 8), ("nBCSVM", 3, 4)]),
        ("6j2t", [("numJets", 6, 8), ("nBCSVM", 2, 3)]),
        ("5j4t", [("numJets", 5, 6), ("nBCSVM", 4, 6)]),
        ("5j3t", [("numJets", 5, 6), ("nBCSVM", 3, 4)]),
        ("4j4t", [("numJets", 4, 5), ("nBCSVM", 4, 5)]),
        ("4j3t", [("numJets", 4, 5), ("nBCSVM", 3, 4)]),
    ]
    for cn, cut in cuts:
        rules_bdt[cn] = ProjectionRule(
            name=cn,
            cuts=cut,
            project_axes=["common_bdt"],
            sample_filter=lambda sn: True,
            output_rename=RenameRule(),
            rebin=4
        )
        rules_mem[cn] = ProjectionRule(
            name=cn,
            cuts=cut,
            project_axes=["mem_SL_0w2h2t"],
            sample_filter=lambda sn: True,
            output_rename=RenameRule(),
            rebin=6
        )
    
    inputs = OrderedDict()
    for hn, h in hsparse[0].items()+hsparse[1].items()+hsparse[4].items():
        inputs[InputKey(hn, "nominal")] = h
    for sample, systdicts in hsparse[2].items()+hsparse[3].items():
        for systname, hist in systdicts.items():
            inputs[InputKey(sample, systname)] = hist

    out_bdt = apply_rules(
        inputs,
        makeRule_SL(rules_bdt),
    )
    sparse.save_hdict("out_bdt.root", out_bdt)
    inf = rootpy.io.File("out_bdt.root")

    for cn, cut in cuts:
        plt.figure(figsize=(6,6))
        r = plotlib.draw_data_mc(
            inf,
            "{0}/common_bdt/common_bdt".format(cn),
            plotlib.samplelist,
            dataname=["data"],
            xlabel=plotlib.varnames["common_bdt"],
            xunit="",
            legend_fontsize=10, legend_loc="best", colors=[plotlib.colors.get(s[0]) for s in plotlib.samplelist],
            do_legend=True,
            show_overflow=True,
            title_extended="$,\\ \\mathcal{L}=2.6,\\ \\mathrm{fb}^{-1}$, " + cn,
            systematics=[
                ("_CMS_scale_jUp", "_CMS_scale_jDown"),
                ("_CMS_ttH_CSVLFUp", "_CMS_ttH_CSVLFDown"),
                ("_CMS_ttH_CSVHFUp", "_CMS_ttH_CSVHFDown"),
                ("_CMS_ttH_CSVHFStats1Up", "_CMS_ttH_CSVHFStats1Down"),
                ("_CMS_ttH_CSVHFStats2Up", "_CMS_ttH_CSVHFStats2Down"),
                ("_CMS_ttH_CSVLFStats1Up", "_CMS_ttH_CSVLFStats1Down"),
                ("_CMS_ttH_CSVLFStats2Up", "_CMS_ttH_CSVLFStats2Down"),
                ("_CMS_ttH_CSVcErr1Up", "_CMS_ttH_CSVcErr1Down"),
                ("_CMS_ttH_CSVcErr2Up", "_CMS_ttH_CSVcErr2Down"),
            ],
            #blindFunc=blind,
            #do_pseudodata=True
        )
        plotlib.svfg("common_bdt_{0}.png".format(cn))
        plt.clf()

    out_mem = apply_rules(
        inputs,
        makeRule_SL(rules_mem),
    )
    sparse.save_hdict("out_mem.root", out_mem)
