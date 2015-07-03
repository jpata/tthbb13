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
        tf = ROOT.TFile.Open( self.conf.bran["pdfFile"], "READ" )
        h3_b = tf.Get("csv_b_pt_eta")
        h3_c = tf.Get("csv_c_pt_eta")
        h3_l = tf.Get("csv_l_pt_eta")
        btag_pdfs = maptype()
        btag_pdfs[MEM.DistributionType.csv_b] = h3_b
        btag_pdfs[MEM.DistributionType.csv_c] = h3_c
        btag_pdfs[MEM.DistributionType.csv_l] = h3_l
        self.rnd = MEM.BTagRandomizer(0, -1, btag_pdfs, 0)
        self.btagWP = self.conf.jets["btagWPs"][self.conf.jets["btagWP"]][1]

        self.jet_categories = []
        for cat in self.conf.bran["jetCategories"].items():
            print cat[1][0], cat[1][1], self.btagWP, cat[1][2], cat[0]
            jetcat = MEM.JetCategory(cat[1][0], cat[1][1], self.btagWP, cat[1][2], cat[0] )
            self.jet_categories.append( jetcat )
        
        self.vec_jet_categories = vectype()
        for jc in self.jet_categories:
            self.vec_jet_categories.push_back(jc)

        super(BTagRandomizerAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(BTagRandomizerAnalyzer, self).beginLoop(setup)

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            res = self._process(event_syst)
            event.systResults[syst] = res
        return True

    def _process(self, event):
        if "debug" in self.conf.general["verbosity"]:  
            print "BTagRandomizer"

        event.b_ran_results = []

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

        tmp_vec_jet_categories = vectype() 
        for jc in self.vec_jet_categories:
            if jc.ntags_l <= event.numJets:
                tmp_vec_jet_categories.push_back(jc)

        ret = self.rnd.run_all(tmp_vec_jet_categories)

        for k in range(3):
            out = MEM.BTagRandomizerOutput()
            runpos = -1
            for h in range(len(ret)):
                if ret[h].tag_id==k:
                    runpos = h
            if runpos>=0 :
                out = ret[runpos]
            res = [0,0,0,0,0]
            res[0] = out.p
            res[1] = out.ntoys
            res[2] = out.pass_rnd
            res[3] = getattr(out,"pass", 0)
            res[4] = out.tag_id
            event.b_ran_results.append( res )

            b_ranval_results = []
            for j in range(out.n_jets):
                b_ranval_results.append( out.rnd_btag[j] )
            setattr(event, "b_ranval_results_"+out.tag_name, b_ranval_results)

        #for r in event.b_ran_results:
        #    print r.p, r.ntoys

        self.rnd.next_event();

        event.passes_bran = True
        return event
