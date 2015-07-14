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
        self.rnd = MEM.BTagRandomizer(0, -1, btag_pdfs, 1)
        self.btagWP = self.conf.jets["btagWPs"][self.conf.jets["btagWP"]][1]

        self.jet_categories = []
        for cat in self.conf.bran["jetCategories"].items():
            #print cat[1][0], cat[1][1], self.btagWP, cat[1][2], cat[0]
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

        run_vec_jet_categories = vectype() 

        posrun = []
        pos = -1
        for jc in self.vec_jet_categories:
            pos += 1
            if jc.ntags_l <= event.numJets:
                run_vec_jet_categories.push_back(jc)
                posrun.append( pos )

        ret = self.rnd.run_all(run_vec_jet_categories)


        pos    = -1
        for jc in self.vec_jet_categories:            
            pos += 1
            catname = jc.name_tag
            catid   = jc.tag
            out     = MEM.BTagRandomizerOutput()
            wasrun  = pos in posrun
            if wasrun:
                out = ret[ posrun.index(pos) ]
                setattr(event, "b_rnd_results_"+catname, [out.p, out.ntoys, out.pass_rnd,           out.tag_id] )
                setattr(event, "b_inp_results_"+catname, [1.0,           0, getattr(out,"pass",0),  out.tag_id] )
            else:
                setattr(event, "b_rnd_results_"+catname, [0,0,0,0] )
                setattr(event, "b_inp_results_"+catname, [0,0,0,0] )
            #b_rndval_results = []
            #b_inpval_results = []
            for j in range(event.numJets):
                inpval = event.good_jets[j].btagCSV
                rndval = inpval
                if wasrun:
                    inpval = out.input_btag[j] 
                    rndval = out.rnd_btag[j] 
                #b_rndval_results.append( rndval )
                #b_inpval_results.append( inpval )
                setattr(event.good_jets[j], "btagCSVInp"+catname, inpval )
                setattr(event.good_jets[j], "btagCSVRnd"+catname, rndval )
            #setattr(event, "b_rndval_results_"+catname, b_rndval_results)
            #setattr(event, "b_inpval_results_"+catname, b_inpval_results)
            
            countTags = 0
            for jet in event.good_jets: 
                if wasrun and getattr( jet,  "btagCSVRnd"+catname ) > self.btagWP:
                    countTags += 1
            setattr(event, "nBCSVMRnd"+catname, countTags)            

        #for r in event.b_ran_results:
        #    print r.p, r.ntoys

        self.rnd.next_event();

        event.passes_bran = True
        return event