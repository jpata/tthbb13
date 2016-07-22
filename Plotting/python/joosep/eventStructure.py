import ROOT
from rootpy.tree.chain import TreeChain
import sys, os
from collections import OrderedDict
from rootpy.vector import LorentzVector
import rootpy
import rootpy.io

import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix, xsec, samples_nick, xsec_sample, get_prefix_sample

NA = -999
MEM_SF = 0.1

def logit(x):
    return np.log(x/(1.0 - x))

class Func:
    def __init__(self, branch, **kwargs):
        self.branch = branch
        self.func = kwargs.get("func",
            lambda ev, branch=self.branch: getattr(ev, branch)
        )

    def __call__(self, event):
        return self.func(event)

class Var:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.typ = kwargs.get("type")

        #in case function not defined, just use variable name
        self.nominal_func = kwargs.get("nominal", Func(self.name))

        self.systematics_funcs = kwargs.get("systematics", {})


    def getValue(self, event, systematic="nominal"):
        if systematic == "nominal" or not self.systematics_funcs.has_key(systematic):
            return self.nominal_func(event)
        else:
            return self.systematics_funcs[systematic](event)

class Desc:
    def __init__(self, variables=[]):
        self.variables = variables
        self.variables_dict = OrderedDict([(v.name, v) for v in self.variables])

    def getValue(self, event, systematic="nominal"):
        ret = OrderedDict()
        for vname, v in self.variables_dict.items():
            ret[vname] = v.getValue(event, systematic)
        return ret

def event_as_str(ret):
    NA = "NA"
    ret2 = {}
    ret2.update(ret)
    ret2["jets_p4_spherical"] = ",\n".join([
        "    jet(pt={:.2f} eta={:.2f} phi={:.2f} m={:.2f})".format(
            lv.Pt(), lv.Eta(), lv.Phi(), lv.M()
        ) for lv in ret["jets_p4"]
    ])

    r = """
Event(
  run:lumi:event = {run}:{lumi}:{evt}
  syst = {syst}
  numJets = {numJets}
  nBCSVM = {nBCSVM} nBCMVAM = {nBCMVAM}
  blr_CSV = {btag_LR_4b_2b_btagCSV_logit:.2f} blr_cMVA = {btag_LR_4b_2b_btagCMVA_logit:.2f}
  jets_p4 =
{jets_p4_spherical}
  mem_SL_0w2h2t_p = {mem_SL_0w2h2t_p:.4f} mem_SL_1w2h2t_p = {mem_SL_1w2h2t_p:.4f} mem_SL_2w2h2t_p = {mem_SL_2w2h2t_p:.4f}
  ttCls = {ttCls}
)
""".format(**ret2).strip()
    return r

def lv_p4s(pt, eta, phi, m):
    ret = LorentzVector()
    ret.SetPtEtaPhiM(pt, eta, phi, m)
    return ret

desc = Desc([
    Var(name="run"),
    Var(name="lumi"),
    Var(name="evt"),

    Var(name="is_sl"),
    Var(name="is_dl"),

    Var(name="numJets"),
    Var(name="nBCSVM"),
    Var(name="nBCMVAM"),

    Var(name="ttCls"),

    Var(name="btag_LR_4b_2b_btagCSV_logit",
        nominal=Func("blr_CSV", func=lambda ev: logit(ev.btag_LR_4b_2b_btagCSV)),
    ),
    Var(name="btag_LR_4b_2b_btagCMVA_logit",
        nominal=Func("blr_cMVA", func=lambda ev: logit(ev.btag_LR_4b_2b_btagCMVA)),
    ),

    Var(name="nBCMVAM"),

    Var(name="jets_p4",
        nominal=Func(
            "jets_p4",
            func=lambda ev: [lv_p4s(pt, eta, phi, m) for (pt, eta, phi, m) in
            zip(ev.jets_pt[:ev.njets], ev.jets_eta[:ev.njets], ev.jets_phi[:ev.njets], ev.jets_mass[:ev.njets])]
        ),
        systematics = {
            "JESUp": Func(
                "jets_p4_JESUp",
                func=lambda ev: [lv_p4s(pt*float(cvar)/float(c), eta, phi, m) for (pt, eta, phi, m, cvar, c) in
                zip(ev.jets_pt[:ev.njets], ev.jets_eta[:ev.njets], ev.jets_phi[:ev.njets], ev.jets_mass[:ev.njets], ev.jets_corr_JESUp[:ev.njets], ev.jets_corr[:ev.njets])]
            ),
            "JESDown": Func(
                "jets_p4_JESDown",
                func=lambda ev: [lv_p4s(pt*float(cvar)/float(c), eta, phi, m) for (pt, eta, phi, m, cvar, c) in
                zip(ev.jets_pt[:ev.njets], ev.jets_eta[:ev.njets], ev.jets_phi[:ev.njets], ev.jets_mass[:ev.njets], ev.jets_corr_JESDown[:ev.njets], ev.jets_corr[:ev.njets])]
            )
        }
    ),

    Var(name="mem_SL_0w2h2t_p",
        nominal=Func("mem_p_SL_0w2h2t", func=lambda ev, sf=MEM_SF: ev.mem_tth_SL_0w2h2t_p/(ev.mem_tth_SL_0w2h2t_p + sf*ev.mem_ttbb_SL_0w2h2t_p) if ev.mem_tth_SL_0w2h2t_p>0 else 0.0),
    ),
    Var(name="mem_SL_1w2h2t_p",
        nominal=Func("mem_p_SL_1w2h2t", func=lambda ev, sf=MEM_SF: ev.mem_tth_SL_1w2h2t_p/(ev.mem_tth_SL_1w2h2t_p + sf*ev.mem_ttbb_SL_1w2h2t_p) if ev.mem_tth_SL_1w2h2t_p>0 else 0.0),
    ),
    Var(name="mem_SL_2w2h2t_p",
        nominal=Func("mem_p_SL_2w2h2t", func=lambda ev, sf=MEM_SF: ev.mem_tth_SL_2w2h2t_p/(ev.mem_tth_SL_2w2h2t_p + sf*ev.mem_ttbb_SL_2w2h2t_p) if ev.mem_tth_SL_2w2h2t_p>0 else 0.0),
    ),
    Var(name="mem_DL_0w2h2t_p",
        nominal=Func("mem_p_DL_0w2h2t", func=lambda ev, sf=MEM_SF: ev.mem_tth_DL_0w2h2t_p/(ev.mem_tth_DL_0w2h2t_p + sf*ev.mem_ttbb_DL_0w2h2t_p) if ev.mem_tth_DL_0w2h2t_p>0 else 0.0),
    ),
])

class Axis:
    def __init__(self, nbins, lo, hi, func):
        self.nbins = nbins 
        self.lo = lo
        self.hi = hi
        self.func = func

    def getValue(self, event):
        return self.func(event)

class SparseOut:
    def __init__(self, name, cut, axes, outdir):
        self.cut = cut
        self.axes = axes

        nbinVec = getattr(ROOT, "std::vector<int>")()
        minVec = getattr(ROOT, "std::vector<double>")()
        maxVec = getattr(ROOT, "std::vector<double>")()
        for ax in axes:
            nbinVec.push_back(ax.nbins)
            minVec.push_back(ax.lo)
            maxVec.push_back(ax.hi)

        self.hist = ROOT.THnSparseF(
            name,
            name,
            len(axes),
            nbinVec.data(),
            minVec.data(),
            maxVec.data(),
        )
        self.hist.Sumw2()
        outdir.Add(self.hist)
    
    def fill(self, event):
        valVec = getattr(ROOT, "std::vector<float>")()
        for ax in axes:
            valVec.push_back(ax.getValue(event))
        self.hist.Fill(valVec)

axes = [
    Axis(1, 0, 1, lambda ev: ev["counting"]),
    Axis(6, 0, 6, lambda ev: ev["leptonFlavour"]),
    Axis(1, 0, 1, lambda ev: ev["evt"]%2==0),
    Axis(36, 0, 1, lambda ev: ev["mem_SL_2w2h2t_p"]),
    Axis(36, 0, 1, lambda ev: ev["mem_SL_1w2h2t_p"]),
    Axis(36, 0, 1, lambda ev: ev["mem_SL_0w2h2t_p"]),
    Axis(36, 0, 1, lambda ev: ev["mem_DL_0w2h2t_p"]),
    Axis(36, 0, 1, lambda ev: ev["common_bdt"]),
    Axis(5, 3, 8, lambda ev: ev["numJets"]),
    Axis(4, 1, 5, lambda ev: ev["nBCSVM"]),
    Axis(4, 1, 5, lambda ev: ev["nBCMVAM"]),
    Axis(50, -20, 20, lambda ev: ev["btag_LR_4b_2b_btagCSV_logit"]),
    Axis(50, -20, 20, lambda ev: ev["btag_LR_4b_2b_btagCMVA_logit"]),
]

if __name__ == "__main__":
    file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    prefix, sample = get_prefix_sample(os.environ["DATASETPATH"])
    process = samples_nick[sample]
    #of = rootpy.io.File("out.root", "RECREATE")
    #dirs = {}
    #dirs["sl"] = of.mkdir("{0}/sl".format(process), recurse=True)
    #dirs["dl"] = of.mkdir("{0}/dl".format(process), recurse=True)

    outdict_syst = {}
  
    events = TreeChain("tree", file_names, verbose=True)
    #events = ROOT.TChain("tree")
    #for fi in file_names:
    #    events.AddFile(fi)

    systs = ["nominal", "JESUp", "JESDown"]
    for syst in systs: 
        syststr = ""
        if syst != "nominal":
            syststr = "_" + syst

        outdict = {}
        #outdict["sl/sparse"] = SparseOut(
        #    "sparse" + syststr,
        #    lambda ev: ev["is_sl"] == 1,
        #    axes,
        #    dirs["sl"] 
        #)
        #outdict["dl/sparse"] = SparseOut(
        #    "sparse" + syststr,
        #    lambda ev: ev["is_dl"] == 1,
        #    axes,
        #    dirs["dl"] 
        #)
        outdict_syst[syst] = outdict

    for iEv, ev in enumerate(events):

        if not ev.is_sl or ev.is_dl:
            continue
        if not ev.numJets >= 4:
            continue
        if not ev.nBCSVM>=3:
            continue

        for syst in systs:
            ret = desc.getValue(ev, syst)
            ret["syst"] = syst
            ret["counting"] = 0
            ret["leptonFlavour"] = 0
            ret["common_bdt"] = 0
            print event_as_str(ret)+"\n---"
            
            #for (k, v) in outdict_syst[syst].items():
            #    if v.cut(ret):
            #        v.fill(ret)

    print "writing output" 
    #of.Write()
    #of.Close()
    #del of
    #del events
