import ROOT
import copy
ROOT.gSystem.Load("libTTHCommonClassifier")

from TTH.MEAnalysis.Analyzer import FilterAnalyzer

CvectorTLorentzVector = getattr(ROOT, "std::vector<TLorentzVector>")
Cvectordouble = getattr(ROOT, "std::vector<double>")
from TTH.MEAnalysis.vhbb_utils import lvec


class CommonClassifierAnalyzer(FilterAnalyzer):
    """
    Performs ME categorization
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(CommonClassifierAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.bdtcalc = ROOT.BDTClassifier()
        self.memcalc = ROOT.MEMClassifier()

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_wtag:
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_mecat = False
        return self.conf.general["passall"] or np.any([v.passes_mecat for v in event.systResults.values()])

    def _process(self, event):

        selectedLeptonP4 = CvectorTLorentzVector()
        selectedLeptonCharge = Cvectordouble()

        selectedJetsP4 = CvectorTLorentzVector()
        selectedJetsCSV = Cvectordouble()
        looseJetsP4 = CvectorTLorentzVector()
        looseJetsCSV = Cvectordouble()

        for lep in event.good_leptons:
            selectedLeptonP4.push_back(lvec(lep))
            selectedLeptonCharge.push_back(lep.charge)

        for jet in event.good_jets:
            selectedJetsP4.push_back(lvec(jet))
            selectedJetsCSV.push_back(jet.btagCSV)
            looseJetsP4.push_back(lvec(jet))
            looseJetsCSV.push_back(jet.btagCSV)

        for jet in event.loose_jets:
            looseJetsP4.push_back(lvec(jet))
            looseJetsCSV.push_back(jet.btagCSV)

        metP4s = CvectorTLorentzVector()
        met_p4 = ROOT.TLorentzVector()
        met_p4.SetPtEtaPhiM(event.MET.pt, 0, event.MET.phi, 0)
        metP4s.push_back(met_p4)

        event.common_mem = []
        event.common_bdt = -2.0

        if event.category_string.startswith("sl_"):
            bdt = self.bdtcalc.GetBDTOutput(selectedLeptonP4, selectedJetsP4, selectedJetsCSV, looseJetsP4, looseJetsCSV, met_p4)
            #mem = self.memcalc.GetOutput(selectedLeptonP4, selectedLeptonCharge, selectedJetsP4, selectedJetsCSV, looseJetsP4, looseJetsCSV, met_p4)
            event.common_bdt = bdt
            #event.common_mem = [mem]

        return event
