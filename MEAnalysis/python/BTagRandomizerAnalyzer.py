from TTH.MEAnalysis.vhbb_utils import lvec
from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.MEMUtils import add_obj
import ROOT
import copy
import numpy as np
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")

import ROOT.MEM as MEM

maptype = getattr(ROOT, "std::map<MEM::DistributionType::DistributionType, TH3D>")
vectype = getattr(ROOT, "std::vector<MEM::JetCategory>")
class BTagRandomizerAnalyzer(FilterAnalyzer):
    """
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        tf = ROOT.TFile.Open("MEAnalysis/root/ControlPlotsV6.root","READ");
        h3_b = tf.Get("csv_b_pt_eta");
        h3_c = tf.Get("csv_c_pt_eta");
        h3_l = tf.Get("csv_l_pt_eta");
        btag_pdfs = maptype()
        btag_pdfs[MEM.DistributionType.csv_b] = h3_b
        btag_pdfs[MEM.DistributionType.csv_c] = h3_c
        btag_pdfs[MEM.DistributionType.csv_l] = h3_l
        self.rnd = MEM.BTagRandomizer(0, -1, btag_pdfs, 1)
        self.btagWP = self.conf.jets["btagWPs"][self.conf.jets["btagWP"]]

        self.jet_categories = [
            MEM.JetCategory(0, 0, 0.879, 0, "6j0t"),
            MEM.JetCategory(1, 1, 0.879, 1, "6j1t"),
            MEM.JetCategory(2, 2, 0.879, 2, "6j2t"),
            MEM.JetCategory(3, 3, 0.879, 3, "6j3t"),
            MEM.JetCategory(4,-1, 0.879, 4, "6jge4t"),
        ]
        self.vec_jet_categories = vectype()
        for jc in self.jet_categories:
            self.vec_jet_categories.push_back(jc)

        super(BTagRandomizerAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(BTagRandomizerAnalyzer, self).beginLoop(setup)

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_btag:
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_mva = False
        return True

    def _process(self, event):
        print "BTagRandomizer"
        for jet in event.good_jets:
            add_obj(
                self.rnd,
                MEM.ObjectType.Jet,
                p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                obs_dict={
                    MEM.Observable.BTAG: jet.btagCSV > self.btagWP,
                    MEM.Observable.PDGID: jet.mcFlavour,
                    MEM.Observable.CSV: jet.btagCSV
                }
            )
        ret = self.rnd.run_all(self.vec_jet_categories)
        for r in ret:
            print r.p, r.ntoys
        self.rnd.next_event();
        return event
