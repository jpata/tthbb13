import ROOT
import sys, os, json, math, copy
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample
from PhysicsTools.HeppyCore.statistics.tree import Tree
import numpy as np

class Correction:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name")
        self.nominal = kwargs.get("nominal")
        self.variated = kwargs.get("variated")

class Jet:
    def __init__(self, *args, **kwargs):
        self.pt = kwargs.get("pt")
        self.eta = kwargs.get("eta")
        self.phi = kwargs.get("phi")
        self.mass = kwargs.get("mass")

        self.csv = kwargs.get("csv")
        self.cmva = kwargs.get("cmva")
        self.corrections = kwargs.get("corrections")

    def correct(self, correction):
        return Jet(
            pt = correction.variated * self.pt / correction.nominal if correction.nominal > 0 else self.pt,
            eta = self.eta,
            phi = self.phi,
            mass = correction.variated * self.mass / correction.nominal if correction.nominal > 0 else self.mass,
            csv = self.csv,
            cmva = self.cmva,
            corrections = self.corrections
        )

def make_corrections(event, schema, jet_base, ijet):
    corrs = []

    corrs += [Correction(
        name = "nominal",
        nominal=1.0,
        variated=1.0,
    )]

    if schema == "mc":
        for nominal, variated in [
            ("corr", "JESUp"),
            ("corr", "JESDown"),
            ("corr_JER", "JERUp"),
            ("corr_JER", "JERDown"),
        ]:
            corrs += [
                Correction(
                    name = variated,
                    nominal=getattr(event, "{0}_{1}".format(jet_base, nominal))[ijet],
                    variated=getattr(event, "{0}_{1}".format(jet_base, "corr_" + variated))[ijet],
                )
            ]
    return corrs

class Scenario:
    def __init__(self, *args, **kwargs):
        self.jets = kwargs.get("jets")
        self.leps_p4 = kwargs.get("leps_p4")
        self.leps_charge = kwargs.get("leps_charge")
        self.met_pt = kwargs.get("met_pt")
        self.met_phi = kwargs.get("met_phi")
        self.systematic_index = kwargs.get("systematic_index")

if __name__ == "__main__":
    from TTH.Plotting.Datacards.AnalysisSpecificationFromConfig import analysisFromConfig

    if os.environ.has_key("FILE_NAMES"):
        file_names = map(getSitePrefix, os.environ["FILE_NAMES"].split())
        prefix, sample_name = get_prefix_sample(os.environ["DATASETPATH"])
        an_name, analysis = analysisFromConfig(os.environ.get("ANALYSIS_CONFIG"))
    else:
        file_names = map(getSitePrefix, [
            "/store/user/jpata/tth/Sep14_leptonic_nome_v1/ttHTobb_M125_13TeV_powheg_pythia8/Sep14_leptonic_nome_v1/160914_142604/0000/tree_1.root"
        ])
        prefix = ""
        sample_name = "ttHTobb_M125_13TeV_powheg_pythia8"
        an_name, analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/Plotting/python/Datacards/config_sldl.cfg")

    sample = analysis.get_sample(sample_name)

    ch = ROOT.TChain("tree")
    for fi in file_names:
        ch.AddFile(getSitePrefix(fi))
    
    outfile = ROOT.TFile('out.root', 'recreate')
    tree = Tree('tree', 'MEM tree')
    tree.var('systematic', type=int)
    tree.var('njets', type=int)
    max_jets = 10
    for v in ["jet_pt", "jet_eta", "jet_phi", "jet_mass", "jet_csv", "jet_cmva"]:
        tree.vector(v, "njets", maxlen=max_jets, type=float, storageType="F")

    for v in ["jet_type"]:
        tree.vector(v, "njets", maxlen=max_jets, type=int, storageType="i")
    
    max_leps = 2
    tree.var('nleps', type=int)
    for v in ["lep_pt", "lep_eta", "lep_phi", "lep_mass", "lep_charge"]:
        tree.vector(v, "nleps", maxlen=max_leps, type=float, storageType="F")
    
    tree.var('met_pt', type=float, storageType="F")
    tree.var('met_phi', type=float, storageType="F")
    
    tree.var('hypothesis', type=int, storageType="I")
   
    for v in ["event", "run", "lumi"]:
        tree.var(v, type=int, storageType="L")

    for iEv, ev in enumerate(ch):
        accept = (ev.is_sl and ev.njets >= 4 and (ev.nBCSVM >= 3 or ev.nBCMVAM >= 3))
        accept = accept or (ev.is_dl and ev.njets >= 4 and (ev.nBCSVM >= 3 or ev.nBCMVAM >= 3))

        if not accept:
            continue
        hypo = -1

        leps_p4 = []
        leps_charge = []
        for ilep in range(ev.nleps)[:max_leps]:
            p4 = [
                ev.leps_pt[ilep],
                ev.leps_eta[ilep],
                ev.leps_phi[ilep],
                ev.leps_mass[ilep]
            ]
            leps_p4 += [p4]
            leps_charge += [math.copysign(1, ev.leps_pdgId[ilep])]
 
        jets = []

        for ijet in range(ev.njets)[:max_jets]:
            jets += [Jet(
                pt = ev.jets_pt[ijet],
                eta = ev.jets_eta[ijet],
                phi = ev.jets_phi[ijet],
                mass = ev.jets_mass[ijet],
                csv = ev.jets_btagCSV[ijet],
                cmva = ev.jets_btagCMVA[ijet],
                corrections = make_corrections(ev, sample.schema, "jets", ijet)
            )]

        scenarios = []
        for isf in range(len(jets[0].corrections)):
            scenario = Scenario(
                jets = [j.correct(j.corrections[isf]) for j in jets],
                leps_p4 = leps_p4,
                leps_charge = leps_charge,
                met_pt = ev.met_pt,
                met_phi = ev.met_phi,
                systematic_index = isf
            )
            scenarios += [scenario]

        for scenario in scenarios:
            tree.fill('njets', len(scenario.jets))
            tree.vfill('jet_pt', [x.pt for x in scenario.jets])
            tree.vfill('jet_eta', [x.eta for x in scenario.jets])
            tree.vfill('jet_phi', [x.phi for x in scenario.jets])
            tree.vfill('jet_mass', [x.mass for x in scenario.jets])
            tree.vfill('jet_csv', [x.csv for x in scenario.jets])
            tree.vfill('jet_cmva', [x.cmva for x in scenario.jets])

            tree.fill('nleps', len(scenario.leps_p4))
            tree.vfill('lep_pt', [x[0] for x in scenario.leps_p4])
            tree.vfill('lep_eta', [x[1] for x in scenario.leps_p4])
            tree.vfill('lep_phi', [x[2] for x in scenario.leps_p4])
            tree.vfill('lep_mass', [x[3] for x in scenario.leps_p4])
            tree.vfill('lep_charge', scenario.leps_charge)
            
            tree.fill('met_pt', scenario.met_pt)
            tree.fill('met_phi', scenario.met_phi)
            
            tree.fill('event', ev.evt)
            tree.fill('run', ev.run)
            tree.fill('lumi', ev.lumi)
            
            tree.fill('systematic', scenario.systematic_index)
            tree.fill('hypothesis', hypo)
            
            tree.tree.Fill()
    
    outfile.Write()
