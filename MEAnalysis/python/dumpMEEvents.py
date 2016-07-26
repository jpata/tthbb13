import ROOT
import sys, os, json
from TTH.MEAnalysis.samples_base import getSitePrefix
import math

DATASETPATH = os.environ["DATASETPATH"]
FILE_NAMES = os.environ["FILE_NAMES"].split()

ch = ROOT.TChain("tree")
for fi in FILE_NAMES:
    ch.AddFile(getSitePrefix(fi))

for ev in ch:
    if not (ev.is_sl and ev.numJets==6 and ev.nBCSVM==4):
        continue

    jets_p4 = []
    jets_btag = []
    jets_csv = []
    jets_cmva = []
    jets_matchFlag = []
    jets_hadronFlavour = []
    for ijet in range(ev.numJets):
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
        jets_hadronFlavour += [ev.jets_hadronFlavour[ijet]]
        jets_matchFlag += [ev.jets_matchFlag[ijet]]
    
    leps_p4 = []
    leps_charge = []
    for ilep in range(ev.nleps):
        p4 = [
            ev.leps_pt[ilep],
            ev.leps_eta[ilep],
            ev.leps_phi[ilep],
            ev.leps_mass[ilep]
        ]
        leps_p4 += [p4]
        leps_charge += [math.copysign(1, ev.leps_pdgId[ilep])]

    event = {
        "input": {
            "selectedJetsP4": jets_p4,
            "selectedJetsBTag": jets_btag,
            "selectedJetsCSV": jets_csv,
            "selectedJetsCMVA": jets_cmva,
            "selectedJetsMatchFlag": jets_matchFlag,
            "selectedJetsHadronFlavour": jets_hadronFlavour,

            "selectedLeptonsP4": leps_p4,
            "selectedLeptonsCharge": leps_charge,

            "metP4": [ev.met_pt, ev.met_phi],
            "evt": ev.evt,
            "run": ev.run,
            "lumi": ev.lumi,
            "numJets": ev.numJets,
            "nBCSVM": ev.nBCSVM,
            "nBCMVAM": ev.nBCMVAM,
            "btag_LR_4b_2b_btagCSV": ev.btag_LR_4b_2b_btagCSV,
            "btag_LR_4b_2b_btagCMVA": ev.btag_LR_4b_2b_btagCMVA,
            
            "nMatch_wq": ev.nMatch_wq_btag,
            "nMatch_tb": ev.nMatch_tb_btag,
            "nMatch_hb": ev.nMatch_hb_btag,
            "nMatch_wq_btag": ev.nMatch_wq_btag,
            "nMatch_tb_btag": ev.nMatch_tb_btag,
            "nMatch_hb_btag": ev.nMatch_hb_btag,
        }
    }
    print json.dumps(event)
