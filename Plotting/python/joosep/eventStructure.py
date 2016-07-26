import ROOT
ROOT.TH1.AddDirectory(False)
from rootpy.tree.chain import TreeChain
import sys, os
from collections import OrderedDict
from rootpy.vector import LorentzVector
import rootpy
import rootpy.io

import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix, xsec, samples_nick, xsec_sample, get_prefix_sample
from TTH.Plotting.Datacards.sparse import save_hdict

NA = -999
MEM_SF = 0.1

PROCESS_MAP = {
    "ttH_hbb": 0,
    "ttH_nonbb": 1,
    "ttbarPlusBBbar": 2,
    "ttbarPlus2B": 3,
    "ttbarPlusB": 4,
    "ttbarPlusCCbar": 5,
    "ttbarOther": 6,
}

def assign_process_label(process, event):
    """
    In case the you need to decide which process an event falls into based on
    the event itself:
    process (string): the input process
    event (FIXME): the event data

    returns (string): the newly modified process string
    """
    if process == "ttbarUnsplit":
        ttCls = event["ttCls"]
        if ttCls == 51:
            _process = "ttbarPlusB"
        elif ttCls == 52:
            _process = "ttbarPlus2B"
        elif ttCls >= 53:
            _process = "ttbarPlusBBbar"
        elif ttCls in [41, 42, 43, 44, 45]:
            _process = "ttbarPlusCCbar"
        else:
            _process = "ttbarOther"
        process = _process
    return process

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
    def __init__(self, name, nbins, lo, hi, func):
        self.name = name
        self.nbins = nbins 
        self.lo = lo
        self.hi = hi
        self.func = func

    def getValue(self, event):
        return self.func(event)

class SparseOut:
    def __init__(self, name, cut, axes):
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
        for iax, ax in enumerate(self.axes):
            self.hist.GetAxis(iax).SetName(ax.name)
            self.hist.GetAxis(iax).SetTitle(ax.name)

        self.hist.Sumw2()
    
    def fill(self, event):
        valVec = getattr(ROOT, "std::vector<float>")()
        for ax in self.axes:
            v = ax.getValue(event)
            valVec.push_back(v)
        self.hist.Fill(valVec)

def saveResults(outfile, prefix, outdict_syst):
    hdict = {}
    for syst, outdict in outdict_syst.items():
        if syst == "nominal":
            systsuf = ""
        else:
            systsuf = "_" + syst

        for name, obj in outdict.items():
            full_name = "{0}/{1}{2}".format(prefix, name, systsuf)
            print full_name, obj.hist.GetEntries()
            obj.hist = obj.hist.Clone()
            hdict[full_name] = obj.hist
    save_hdict(outfile, hdict)

axes = [
    Axis("process", 20, 0, 20, lambda ev: ev["process"]),
    Axis("counting", 1, 0, 1, lambda ev: ev["counting"]),
    Axis("leptonFlavour", 6, 0, 6, lambda ev: ev["leptonFlavour"]),
    Axis("parity", 1, 0, 1, lambda ev: ev["evt"]%2==0),
    Axis("mem_SL_2w2h2t_p", 36, 0, 1, lambda ev: ev["mem_SL_2w2h2t_p"]),
    Axis("mem_SL_1w2h2t_p", 36, 0, 1, lambda ev: ev["mem_SL_1w2h2t_p"]),
    Axis("mem_SL_0w2h2t_p", 36, 0, 1, lambda ev: ev["mem_SL_0w2h2t_p"]),
    Axis("mem_DL_0w2h2t_p", 36, 0, 1, lambda ev: ev["mem_DL_0w2h2t_p"]),
    Axis("common_bdt", 36, 0, 1, lambda ev: ev["common_bdt"]),
    Axis("numJets", 5, 3, 8, lambda ev: ev["numJets"]),
    Axis("nBCSVM", 4, 1, 5, lambda ev: ev["nBCSVM"]),
    Axis("nBCMVAM", 4, 1, 5, lambda ev: ev["nBCMVAM"]),
    Axis("btag_LR_4b_2b_btagCSV_logit", 50, -20, 20, lambda ev: ev["btag_LR_4b_2b_btagCSV_logit"]),
    Axis("btag_LR_4b_2b_btagCMVA_logit", 50, -20, 20, lambda ev: ev["btag_LR_4b_2b_btagCMVA_logit"]),
    Axis("jetsByPt_0_pt", 50, 0, 400, lambda ev: ev["jets_p4"][0].Pt()),
]

if __name__ == "__main__":
    file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
    prefix, sample = get_prefix_sample(os.environ["DATASETPATH"])
    process = samples_nick[sample]

    outdict_syst = {}
    
    systs = ["nominal", "JESUp", "JESDown"]
    for syst in systs: 
        syststr = ""
        if syst != "nominal":
            syststr = "_" + syst

        outdict = {}
        outdict["sl/sparse"] = SparseOut(
            "sparse" + syststr,
            lambda ev: ev["is_sl"] == 1,
            axes,
        )
        outdict["dl/sparse"] = SparseOut(
            "sparse" + syststr,
            lambda ev: ev["is_dl"] == 1,
            axes,
        )
        outdict_syst[syst] = outdict
    
    nevents = 0
    for file_name in file_names:
        print "opening {0}".format(file_name)
        tf = rootpy.io.File.Open(file_name)
        events = tf.Get("tree")
        print "opened {0}".format(events)
        print "looping over {0} events".format(events.GetEntries())
       
        iEv = 0
        for ev in events:
            if not (ev.is_sl or ev.is_dl):
                continue
            if not ev.numJets >= 4:
                continue
            if not ev.nBCSVM>=3:
                continue

            for syst in systs:
                ret = desc.getValue(ev, syst)
                proc_label = assign_process_label(process, ret)
                ret["process"] = PROCESS_MAP[proc_label]
                ret["syst"] = syst
                ret["counting"] = 0
                ret["leptonFlavour"] = 0
                ret["common_bdt"] = 0
                #print event_as_str(ret)+"\n---"
                
                for (k, v) in outdict_syst[syst].items():
                    if v.cut(ret):
                        v.fill(ret)
            #end of loop over systematics
            nevents += 1
            iEv += 1
        #end of loop over events
        tf.Close()
    #end of loop over file names

    print "processed {0} events".format(nevents)
    print "writing output"

    saveResults("out.root", process, outdict_syst)
