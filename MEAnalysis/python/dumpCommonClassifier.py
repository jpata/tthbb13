import ROOT
import sys, os, json, math, copy
from TTH.MEAnalysis.samples_base import getSitePrefix, get_prefix_sample
from PhysicsTools.HeppyCore.statistics.tree import Tree
import numpy as np

class Scenario:
    def __init__(self, *args, **kwargs):
        self.jets_p4 = kwargs.get("jets_p4")
        self.jets_csv = kwargs.get("jets_csv")
        self.jets_cmva = kwargs.get("jets_cmva")
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
        an_name, analysis = analysisFromConfig(os.environ["CMSSW_BASE"] + "/src/TTH/Plotting/python/Datacards/config_sl.cfg")

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
   
    for v in ["event", "run", "lumi"]:
        tree.var(v, type=int, storageType="L")

    for iEv, ev in enumerate(ch):
        accept = (ev.is_sl and ev.njets >= 4 and ev.nBCSVM >= 3)
        accept = accept or (ev.is_dl and ev.njets >= 4 and ev.nBCSVM >= 3)
        if not accept:
            continue
       
        scenarios = []

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
         
        jets_p4 = []
        jets_btag = []
        jets_csv = []
        jets_cmva = []
        for ijet in range(ev.njets)[:max_jets]:
            p4 = [
                ev.jets_pt[ijet],
                ev.jets_eta[ijet],
                ev.jets_phi[ijet],
                ev.jets_mass[ijet]
            ]
            jets_p4 += [p4]
            jets_btag += [ev.jets_btagFlag[ijet]]
            jets_csv += [ev.jets_btagCSV[ijet]]
            jets_cmva += [ev.jets_btagCMVA[ijet]]

            scale_factors = [
                (0, 1.0),
            ]
            if sample.schema == "mc":
                if ev.jets_corr[ijet]>0:
                    scale_factors += [
                        (1, ev.jets_corr_JESUp[ijet]/ev.jets_corr[ijet]),
                        (2, ev.jets_corr_JESDown[ijet]/ev.jets_corr[ijet]),
                    ]
                else:
                    scale_factors += [
                        (1, 1.0),
                        (2, 1.0),
                    ]
                if ev.jets_corr_JER[ijet]>0:
                    scale_factors += [
                        (3, ev.jets_corr_JERUp[ijet]/ev.jets_corr_JER[ijet]),
                        (4, ev.jets_corr_JERDown[ijet]/ev.jets_corr_JER[ijet]),
                    ]
                else:
                    scale_factors += [
                        (3, 1.0),
                        (4, 1.0),
                    ]
        
        for syst_idx, sf in scale_factors:
            jets_p4_rescaled = []
            for p4 in jets_p4:
                pt_new = sf * p4[0]
                mass_new = sf * p4[3]
                jets_p4_rescaled += [(pt_new, p4[1], p4[2], mass_new)]

            scenario = Scenario(
                jets_p4 = jets_p4_rescaled,
                jets_csv = jets_csv,
                jets_cmva = jets_cmva,
                leps_p4 = leps_p4,
                leps_charge = leps_charge,
                met_pt = ev.met_pt,
                met_phi = ev.met_phi,
                systematic_index = syst_idx
            )
            scenarios += [scenario]

        for scenario in scenarios:
            tree.fill('njets', len(scenario.jets_p4))
            tree.vfill('jet_pt', [x[0] for x in scenario.jets_p4])
            tree.vfill('jet_eta', [x[1] for x in scenario.jets_p4])
            tree.vfill('jet_phi', [x[2] for x in scenario.jets_p4])
            tree.vfill('jet_mass', [x[3] for x in scenario.jets_p4])
            tree.vfill('jet_csv', scenario.jets_csv)
            tree.vfill('jet_cmva', scenario.jets_cmva)
            
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
            
            tree.tree.Fill()
    
    outfile.Write()
