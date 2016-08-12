from __future__ import print_function

import ROOT

import sys, os
from collections import OrderedDict
import logging
LOG_MODULE_NAME = logging.getLogger(__name__)
    
import numpy as np
from TTH.MEAnalysis.samples_base import getSitePrefix, xsec, samples_nick, xsec_sample, get_prefix_sample, PROCESS_MAP, TRIGGERPATH_MAP
from TTH.Plotting.Datacards.sparse import save_hdict

#placeholder value
NA = -999

#default MEM scale factor in the likelihood ratio
MEM_SF = 0.1

SYSTEMATICS_EVENT = [
    "CMS_scale_jUp", "CMS_scale_jDown",
    "CMS_res_jUp", "CMS_res_jDown"
]

"""
Create pairs of (systematic_name, weight function), which will be used on the
nominal event to create reweighted copies of the event. The systematic names
here will define the output histograms like
ttH/sl/sparse -> nominal event
ttH/sl/sparse_CMS_ttH_CSVJESUp -> event with btagWeight with JES up variation
...
"""
systematic_weights = []
btag_weights = []
for sdir in ["up", "down"]:
    for syst in ["cferr1", "cferr2", "hf", "hfstats1", "hfstats2", "jes", "lf", "lfstats1", "lfstats2"]:
        for tagger in ["CSV", "CMVAV2"]:
            bweight = "btagWeight{0}_{1}_{2}".format(tagger, sdir, syst)
            #make systematic outputs consistent in Up/Down naming
            sdir_cap = sdir.capitalize()
            systematic_weights += [
                ("CMS_ttH_{0}{1}{2}".format(tagger, syst, sdir_cap), lambda ev, bweight=bweight: ev["weight_nominal"]/ev["btagWeight"+tagger]*ev[bweight])
            ]
            btag_weights += [bweight]

systematic_weights += [
        ("puUp", lambda ev: ev["weight_nominal"]/ev["puWeight"] * ev["puWeightUp"]),
        ("puDown", lambda ev: ev["weight_nominal"]/ev["puWeight"] * ev["puWeightDown"])
]

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
        return _process 
    elif samples_nick.has_key(process):
        return samples_nick[process]
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

def fillSystSuffix(name, systematics):
    ret = {}
    for syst in systematics:
        for sdir in ["Up", "Down"]:
            suffix = syst+sdir
            ret[suffix] = Func(
                name + "_" + suffix,
                func=lambda ev, suff=suffix, fallback=name: getattr(ev, suff, fallback)
            )
    return ret

class Var:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.typ = kwargs.get("type")

        #in case function not defined, just use variable name
        self.nominal_func = kwargs.get("nominal", Func(self.name))
        self.funcs_schema = kwargs.get("funcs_schema", {})

        self.systematics_funcs = kwargs.get("systematics", {})
        #in case this variable is just a pre-calculated branch on the tree (e.g. numJets),
        #append systematic suffixes to create the systematically variated branches (numJets_JESUp)
        if self.systematics_funcs == "suffix":
            if kwargs.has_key("nominal"):
                raise Exception("don't know how to generate systematic function for non-default nominal")
            self.systematics_funcs = fillSystSuffix(self.name, SYSTEMATICS_EVENT)

        self.schema = kwargs.get("schema", ["mc", "data"])

    def getValue(self, event, schema, systematic="nominal"):
        if systematic == "nominal" or not self.systematics_funcs.has_key(systematic):
            return self.funcs_schema.get(schema, self.nominal_func)(event)
        else:
            return self.systematics_funcs[systematic](event)

class Desc:
    def __init__(self, variables=[]):
        self.variables = variables
        self.variables_dict = OrderedDict([(v.name, v) for v in self.variables])

    def getValue(self, event, schema="mc", systematic="nominal"):
        ret = OrderedDict()
        for vname, v in self.variables_dict.items():
            if schema in v.schema:
                ret[vname] = v.getValue(event, schema, systematic)
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
    ret = ROOT.TLorentzVector()
    ret.SetPtEtaPhiM(pt, eta, phi, m)
    return ret

desc = Desc([
    Var(name="run"),
    Var(name="lumi"),
    Var(name="evt"),

    Var(name="is_sl"),
    Var(name="is_dl"),

    Var(name="numJets", systematics="suffix"),
    Var(name="nBCSVM", systematics="suffix"),
    Var(name="nBCMVAM", systematics="suffix"),
    
    Var(name="Wmass", systematics="suffix"),


    Var(name="btag_LR_4b_2b_btagCSV_logit",
        nominal=Func("blr_CSV", func=lambda ev: logit(ev.btag_LR_4b_2b_btagCSV)),
    ),
    Var(name="btag_LR_4b_2b_btagCMVA_logit",
        nominal=Func("blr_cMVA", func=lambda ev: logit(ev.btag_LR_4b_2b_btagCMVA)),
    ),

    Var(name="leps_pdgId", nominal=Func("leps_pdgId", func=lambda ev: [int(ev.leps_pdgId[i]) for i in range(ev.nleps)])),

    Var(name="jets_p4",
        nominal=Func(
            "jets_p4",
            func=lambda ev: [lv_p4s(ev.jets_pt[i], ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i]) for i in range(ev.njets)]
        ),
        systematics = {
            "CMS_scale_jUp": Func(
                "jets_p4_JESUp",
                func=lambda ev: [lv_p4s(ev.jets_pt[i]*float(ev.jets_corr_JESUp[i])/float(ev.jets_corr[i]), ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i]) for i in range(ev.njets)]
            ),
            "CMS_scale_jDown": Func(
                "jets_p4_JESDown",
                func=lambda ev: [lv_p4s(ev.jets_pt[i]*float(ev.jets_corr_JESDown[i])/float(ev.jets_corr[i]), ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i]) for i in range(ev.njets)]
            ),
            "CMS_res_jUp": Func(
                "jets_p4_JERUp",
                func=lambda ev: [lv_p4s(ev.jets_pt[i]*float(ev.jets_corr_JERUp[i])/float(ev.jets_corr_JER[i]) if ev.jets_corr_JER[i]>0 else 0.0, ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i]) for i in range(ev.njets)]
            ),
            "CMS_res_jDown": Func(
                "jets_p4_JERDown",
                func=lambda ev: [lv_p4s(ev.jets_pt[i]*float(ev.jets_corr_JERDown[i])/float(ev.jets_corr_JER[i]) if ev.jets_corr_JER[i]>0 else 0.0, ev.jets_eta[i], ev.jets_phi[i], ev.jets_mass[i]) for i in range(ev.njets)]
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
    
    Var(name="HLT_ttH_DL_mumu", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_DL_mumu}),
    Var(name="HLT_ttH_DL_elel", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_DL_elel}),
    Var(name="HLT_ttH_DL_elmu", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_DL_elmu}),
    Var(name="HLT_ttH_SL_el", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_SL_el}),
    Var(name="HLT_ttH_SL_mu", funcs_schema={"mc": lambda ev: 1.0, "data": lambda ev: ev.HLT_ttH_SL_mu}),

#MC-only branches
    Var(name="ttCls", schema=["mc"]),
    Var(name="puWeight", schema=["mc"]),
    Var(name="puWeightUp", schema=["mc"]),
    Var(name="puWeightDown", schema=["mc"]),
    Var(name="triggerEmulationWeight", schema=["mc"]),

    #nominal b-tag weight, systematic weights added later
    Var(name="btagWeightCSV", schema=["mc"]),
    Var(name="btagWeightCMVAV2", schema=["mc"]),
    ] + [Var(name=bw, schema=["mc"]) for bw in btag_weights]
)

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
    def __init__(self, name, cut, axes, outdir):
        """
        Creates a sparse histogram.
        name (string): name of the histogram, will also be used for the ROOT file
        cut (function event -> bool): decides if this event should be filled 
        axes (list of Axis objects): defines the axes of this sparse histogram
        outdir (TDirectory): the output directory where the THnSparse will be saved
        """
        self.cut = cut
        self.axes = axes

        #create the bin arrays
        nbinVec = getattr(ROOT, "std::vector<int>")()
        minVec = getattr(ROOT, "std::vector<double>")()
        maxVec = getattr(ROOT, "std::vector<double>")()
        for ax in axes:
            nbinVec.push_back(ax.nbins)
            minVec.push_back(ax.lo)
            maxVec.push_back(ax.hi)
        ROOT.gROOT.cd()
        self.hist = ROOT.THnSparseF(
            name,
            name,
            len(axes),
            nbinVec.data(),
            minVec.data(),
            maxVec.data(),
        )
        #make sure this histogram is saved
        outdir.Add(self.hist)
        for iax, ax in enumerate(self.axes):
            self.hist.GetAxis(iax).SetName(ax.name)
            self.hist.GetAxis(iax).SetTitle(ax.name)

        self.hist.Sumw2()
    
    def fill(self, event, weight=1.0):
        """
        Fill this sparse histogram based on the values defined in the axes.
        event (dict of string->object): the data of this event (under a certain systematic assumption)
        weight (float): weight to be used for this event:w
        
        """
        #Very important: need to use double, not float (despite name THnSparseF pointing to float)
        valVec = getattr(ROOT, "std::vector<double>")()

        #loop over defined axes, calculate values
        for ax in self.axes:
            v = ax.getValue(event)
            valVec.push_back(v)
        #print([v for v in valVec], "w={0}".format(weight))

        #Very important: here we need to take the pointer to the start of the value vector with std::vector<double)::data() -> double*
        #otherwise the THnSparse is filled, but with garbage and will result in TBrowser segfaults later 
        return self.hist.Fill(valVec.data(), weight)

axes = [
    Axis("process", 20, 0, 20, lambda ev: ev["process"]),
    Axis("triggerPath", 20, 0, 20, lambda ev: ev["triggerPath"]),
    Axis("counting", 1, 0, 1, lambda ev: ev["counting"]),
    Axis("parity", 1, 0, 1, lambda ev: ev["evt"]%2==0),
    Axis("mem_SL_2w2h2t_p", 36, 0, 1, lambda ev: ev["mem_SL_2w2h2t_p"]),
    Axis("mem_SL_1w2h2t_p", 36, 0, 1, lambda ev: ev["mem_SL_1w2h2t_p"]),
    Axis("mem_SL_0w2h2t_p", 36, 0, 1, lambda ev: ev["mem_SL_0w2h2t_p"]),
    Axis("mem_DL_0w2h2t_p", 36, 0, 1, lambda ev: ev["mem_DL_0w2h2t_p"]),
    Axis("common_bdt", 36, 0, 1, lambda ev: ev["common_bdt"]),
    Axis("numJets", 5, 3, 8, lambda ev: ev["numJets"]),
    Axis("nBCSVM", 4, 1, 5, lambda ev: ev["nBCSVM"]),
    Axis("nBCMVAM", 4, 1, 5, lambda ev: ev["nBCMVAM"]),
    
    Axis("Wmass", 100, 50, 150, lambda ev: ev["Wmass"]),

    Axis("btag_LR_4b_2b_btagCSV_logit", 50, -20, 20, lambda ev: ev["btag_LR_4b_2b_btagCSV_logit"]),
    Axis("btag_LR_4b_2b_btagCMVA_logit", 50, -20, 20, lambda ev: ev["btag_LR_4b_2b_btagCMVA_logit"]),
    
    Axis("jetsByPt_0_pt", 50, 0, 400, lambda ev: ev["jets_p4"][0].Pt()),
    Axis("jetsByPt_1_pt", 50, 0, 400, lambda ev: ev["jets_p4"][1].Pt()),
    Axis("jetsByPt_2_pt", 50, 0, 400, lambda ev: ev["jets_p4"][2].Pt()),

    Axis("jetsByPt_0_eta", 50, 0, 400, lambda ev: ev["jets_p4"][0].Eta()),
    Axis("jetsByPt_1_eta", 50, 0, 400, lambda ev: ev["jets_p4"][1].Eta()),
    Axis("jetsByPt_2_eta", 50, 0, 400, lambda ev: ev["jets_p4"][2].Eta()),
]

def get_schema(sample):
    process = samples_nick[sample]
    if "data" in process:
        schema = "data"
    else:
        schema = "mc"
    return schema

def createOutputs(dirs, systematics):
    outdict_syst = {}
    for syst in systematics: 
        syststr = ""
        if syst != "nominal":
            syststr = "_" + syst

        outdict = {}
        dirs["sl"].cd()
        outdict["sl/sparse"] = SparseOut(
            "sparse" + syststr,
            lambda ev: ev["is_sl"] == 1,
            axes,
            dirs["sl"]
        )
        dirs["dl"].cd()
        outdict["dl/sparse"] = SparseOut(
            "sparse" + syststr,
            lambda ev: ev["is_dl"] == 1,
            axes,
            dirs["dl"]
        )
        outdict_syst[syst] = outdict
    return outdict_syst

def pass_HLT_sl_mu(event):
    pass_hlt = event["HLT_ttH_SL_mu"]
    return event["is_sl"] and pass_hlt and abs(event["leps_pdgId"][0]) == 13

def pass_HLT_sl_el(event):
    pass_hlt = event["HLT_ttH_SL_el"]
    return event["is_sl"] and pass_hlt and abs(event["leps_pdgId"][0]) == 11

def pass_HLT_dl_mumu(event):
    pass_hlt = event["HLT_ttH_DL_mumu"]
    st = sum(map(abs, event["leps_pdgId"]))
    return event["is_dl"] and pass_hlt and st == 26

def pass_HLT_dl_elmu(event):
    pass_hlt = event["HLT_ttH_DL_elmu"]
    st = sum(map(abs, event["leps_pdgId"]))
    return event["is_dl"] and pass_hlt and st == 24

def pass_HLT_dl_elel(event):
    pass_hlt = event["HLT_ttH_DL_elel"]
    st = sum(map(abs, event["leps_pdgId"]))
    return event["is_dl"] and pass_hlt and st == 22

def triggerPath(event):
    if event["is_sl"] and pass_HLT_sl_mu(event):
        return TRIGGERPATH_MAP["m"]
    elif event["is_sl"] and pass_HLT_sl_el(event):
        return TRIGGERPATH_MAP["e"]
    elif event["is_dl"] and pass_HLT_dl_mumu(event):
        return TRIGGERPATH_MAP["mm"]
    elif event["is_dl"] and pass_HLT_dl_elmu(event):
        return TRIGGERPATH_MAP["em"]
    elif event["is_dl"] and pass_HLT_dl_elel(event):
        return TRIGGERPATH_MAP["ee"]
    return 0

if __name__ == "__main__":
    
    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
        prefix, sample = get_prefix_sample(os.environ["DATASETPATH"])
        skip_events = int(os.environ.get("SKIP_EVENTS", 0))
        max_events = int(os.environ.get("MAX_EVENTS", 0))
    else:
        file_names = [getSitePrefix("/store/user/jpata/tth/tth_Aug3_V24_v2/SingleMuon/tth_Aug3_V24_v2/160803_115959/0000/tree_{0}.root").format(i) for i in [10, 105, 106]]
        prefix = ""
        sample = "ttHTobb_M125_13TeV_powheg_pythia8"
        skip_events = 0
        max_events = 10000

    if len(file_names) == 0:
        raise Exception("No files specified, probably a mistake")
    if max_events == 0:
        raise Exception("No events specified, probably a mistake")

    process = samples_nick[sample]
    schema = get_schema(sample)

    #configure systematic scenarios according to MC/Data
    if schema == "mc":
        systematics_event = ["nominal"] + SYSTEMATICS_EVENT
        systematics_weight = [k[0] for k in systematic_weights]
    elif schema == "data":
        systematics_event = ["nominal"]
        systematics_weight = []
   
    dirs = {}
    outfile = ROOT.TFile("out.root", "RECREATE")
    dirs["sample"] = outfile.mkdir(sample)
    dirs["sample"].cd()
    dirs["sl"] = dirs["sample"].mkdir("sl")
    dirs["dl"] = dirs["sample"].mkdir("dl")
    
    #pre-create output histograms
    outdict_syst = createOutputs(dirs, systematics_event+systematics_weight)

    nevents = 0
    counters = OrderedDict()
    counters["triggerPath"] = {}

    for file_name in file_names:
        print("opening {0}".format(file_name))
        tf = ROOT.TFile.Open(file_name)
        events = tf.Get("tree")
        print("opened {0}".format(events))
        print("looping over {0} events".format(events.GetEntries()))
       
        iEv = 0

        for event in events:
            nevents += 1
            iEv += 1
            if nevents < skip_events:
                continue
            if nevents > (skip_events + max_events):
                logging.info("event loop: breaking due to MAX_EVENTS: {0} > {1} + {2}".format(
                    nevents, skip_events, max_events
                ))
                break

            #apply some basic preselection
            if not (event.is_sl or event.is_dl):
                continue
            if not event.numJets >= 3:
                continue
            if not (event.nBCSVM>=2 or event.nBCMVAM>=2):
                continue
            if schema == "data" and not event.json:
                continue

            for syst in systematics_event:
                ret = desc.getValue(event, schema, syst)
                proc_label = assign_process_label(process, ret)
                ret["process"] = PROCESS_MAP[proc_label]
                ret["syst"] = syst
                ret["counting"] = 0
                ret["leptonFlavour"] = 0
                ret["common_bdt"] = 0
                ret["triggerPath"] = triggerPath(ret)
                if not counters["triggerPath"].has_key(ret["triggerPath"]):
                    counters["triggerPath"][ret["triggerPath"]] = 0
                counters["triggerPath"][ret["triggerPath"]] += 1

                ret["weight_nominal"] = 1.0
                if schema == "mc":
                    ret["weight_nominal"] *= ret["puWeight"] * ret["btagWeightCSV"] * ret["triggerEmulationWeight"]
                
                #Fill the base histogram
                for (k, v) in outdict_syst[syst].items():
                    weight = ret["weight_nominal"]
                    if v.cut(ret):
                        v.fill(ret, weight)
               
                #nominal event, fill also histograms with systematic weights
                if syst == "nominal" and schema == "mc":
                    for (syst_weight, weightfunc) in systematic_weights:
                        weight = weightfunc(ret)
                        for (k, v) in outdict_syst[syst_weight].items():
                            if v.cut(ret):
                                v.fill(ret, weight)

            #end of loop over event systematics
        #end of loop over events
        tf.Close()
    #end of loop over file names

    print("processed {0} events".format(nevents))
    print("writing output")
    print(counters)
    outfile.Write()
    outfile.Close()
