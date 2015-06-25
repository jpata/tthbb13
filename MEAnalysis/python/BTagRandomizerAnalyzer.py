from TTH.MEAnalysis.vhbb_utils import lvec
from TTH.MEAnalysis.Analyzer import FilterAnalyzer
import ROOT
import copy
import numpy as np
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")

import ROOT.MEM as MEM

maptype = getattr(ROOT, "std::map<MEM::DistributionType::DistributionType, TH3D>")
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
        return event
