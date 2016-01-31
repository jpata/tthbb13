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
        self.bdtcalc_sl = ROOT.BDTClassifier()
        self.bdtcalc_sl_mem1 = ROOT.MEMBDTClassifier()
        self.bdtcalc_sl_mem2 = ROOT.MEMBDTClassifierV2()
        self.bdtcalc_dl = ROOT.DLBDTClassifier()
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

        event.common_mem = [ROOT.MEMResult()]
        event.common_bdt = -2.0
        event.common_bdt_withmem1 = -2.0
        event.common_bdt_withmem2 = -2.0
        
        if event.category_string.startswith("sl_"):
            event.common_bdt = self.bdtcalc_sl.GetBDTOutput(selectedLeptonP4, selectedJetsP4, selectedJetsCSV, looseJetsP4, looseJetsCSV, met_p4)
            if hasattr(event, "mem_results_tth"):
                mem_p_sig = event.mem_results_tth[self.conf.mem["methodOrder"].index("SL_0w2h2t")]
                mem_p_bkg = event.mem_results_ttbb[self.conf.mem["methodOrder"].index("SL_0w2h2t")]
                event.common_bdt_withmem1 = self.bdtcalc_sl_mem1.GetBDTOutput(
                    selectedLeptonP4, selectedJetsP4, selectedJetsCSV, looseJetsP4, looseJetsCSV, met_p4,
                    mem_p_sig.p/(mem_p_sig.p + 0.15 * mem_p_bkg.p)
                )
                event.common_bdt_withmem2 = self.bdtcalc_sl_mem2.GetBDTOutput(
                    selectedLeptonP4, selectedJetsP4, selectedJetsCSV, looseJetsP4, looseJetsCSV, met_p4,
                    mem_p_sig.p, mem_p_bkg.p
                )
            #mem = self.memcalc.GetOutput(selectedLeptonP4, selectedLeptonCharge, selectedJetsP4, selectedJetsCSV, looseJetsP4, looseJetsCSV, met_p4)
            #event.common_mem = [mem]
        if event.category_string.startswith("dl_"):
            bdt = self.bdtcalc_dl.GetBDTOutput(selectedLeptonP4, selectedLeptonCharge, selectedJetsP4, selectedJetsCSV, met_p4)
            event.common_bdt = bdt
        if "debug" in self.conf.general["verbosity"]:
            print "bdt", event.category_string, event.common_bdt
        return event
