import ROOT
import itertools
import numpy as np

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import lvec, autolog

class QGLRAnalyzer(FilterAnalyzer):
    """
    Performs QG likelihood ratio calculations 
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(QGLRAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.bTagAlgo = self.conf.jets["btagAlgo"]
        self.qglplots_flavour = ROOT.TFile(self.conf.general["QGLPlotsFile_flavour"])
      
        self.qgl_flavour_pdfs = {
        }
        for x in ["q","g"]:
            if (x=="q"):
                self.qgl_flavour_pdfs[x] = self.qglplots_flavour.Get(
                    "hflavour_qgl_0_3"
                )
            else:
                self.qgl_flavour_pdfs[x] = self.qglplots_flavour.Get(
                    "hflavour_qgl_0_0"
                )
            self.qgl_flavour_pdfs[x].Scale(1.0 / self.qgl_flavour_pdfs[x].Integral())

    def get_pdf_prob(self, flavour, pt, eta, qgl, kind):

      
        if kind == "flavour":
            h = self.qgl_flavour_pdfs[(flavour)]

        assert h != None, "flavour={0} kind={1}".format(flavour, kind)
      

        if qgl <0:
            qgl = 0.0
        if qgl > 1.0:
            qgl = 1.0
      
        if (kind == "flavour"):        
            nb = h.FindBin(qgl)
            ret = h.GetBinContent(nb)
        return ret

    def beginLoop(self, setup):
        super(QGLRAnalyzer, self).beginLoop(setup)

    def evaluate_jet_prob(self, pt, eta, qgl, kind):
        return (
            self.get_pdf_prob("q", pt, eta, qgl, kind),
            self.get_pdf_prob("g", pt, eta, qgl, kind)
        )

    def qg_likelihood(self, probs, nQ):

        perms = itertools.permutations(range(len(probs)))

        P = 0.0
        max_p = -1.0
        nperms = 0
        best_perm = None
    
        for perm in perms:
            #print "permutation ",perm
            p = 1.0
             
            maxj = 4
            if (len(probs)<4):
                maxj = len(probs)

            for i in range(0, nQ):
                p *= probs[perm[i]][0]
                #print "ps ",i, p
            for i in range(nQ, maxj):
                p *= probs[perm[i]][1]
                #print "pb ",i, p

            #print nperms, p, perm, max_p, best_perm
            if p > max_p:
                best_perm = perm
                max_p = p

            P += p
            nperms += 1
        P = P / float(nperms)
        assert nperms > 0
        return P, best_perm
        #end permutation loop
 
    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_btag:
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_qgl = False
        return np.any([v.passes_qgl for v in event.systResults.values()])

    def _process(self, event): 
        if "debug" in self.conf.general["verbosity"]:
            autolog("QGLRAnalyzer started")
        event.passes_qgl = True
        if not self.conf.general["doQGL"]:
            return event

        jets_for_qg_lr = event.buntagged_jets_bdisc[0:6]
      
        jet_probs = {
            kind: [
                self.evaluate_jet_prob(j.pt, j.eta, j.qgl, kind)
                for j in jets_for_qg_lr
            ]
            for kind in [
                "flavour"
            ]
        }

        best_4q_perm = 0
        best_0q_perm = 0
        best_flavour_4q_perm = 0
        best_flavour_3q_perm = 0
        best_flavour_2q_perm = 0
        best_flavour_1q_perm = 0
        best_flavour_0q_perm = 0

        nqs4 = 4
        if (len(jets_for_qg_lr)<4):
            nqs4 = len(jets_for_qg_lr)   

        nqs3 = 3
        if (len(jets_for_qg_lr)<3):
            nqs3 = len(jets_for_qg_lr)

        nqs2 = 2
        if (len(jets_for_qg_lr)<2):
            nqs2 = len(jets_for_qg_lr) 
        
        nqs1 = 1
        if (len(jets_for_qg_lr)<1):
            nqs1 = len(jets_for_qg_lr)
    

        event.qg_lr_flavour_4q, best_flavour_4q_perm = self.qg_likelihood(jet_probs["flavour"], nqs4)
        event.qg_lr_flavour_3q, best_flavour_3q_perm = self.qg_likelihood(jet_probs["flavour"], nqs3)
        event.qg_lr_flavour_2q, best_flavour_2q_perm = self.qg_likelihood(jet_probs["flavour"], nqs2)
        event.qg_lr_flavour_1q, best_flavour_1q_perm = self.qg_likelihood(jet_probs["flavour"], nqs1)
        event.qg_lr_flavour_0q, best_flavour_0q_perm = self.qg_likelihood(jet_probs["flavour"], 0)

        def lratio(l1, l2):
            if l1+l2>0:
                return l1/(l1+l2)
            else:
                return 0.0

        def lratio2(l1, l2, l3):
            if l1+l2+l3>0:
                return l1/(l1+l2+l3)
            else:
                return 0.0

        def lratio3(l1, l2, l3, l4):
            if l1+l2+l3+l4>0:
                return l1/(l1+l2+l3+l4)
            else:
                return 0.0 

        def lratio4(l1, l2, l3, l4, l5):
            if l1+l2+l3+l4+l5>0:
                return l1/(l1+l2+l3+l4+l5)
            else:
                return 0.0   
       

        event.qg_LR_flavour_4q_0q =  lratio(event.qg_lr_flavour_4q, event.qg_lr_flavour_0q)
        event.qg_LR_flavour_4q_1q =  lratio(event.qg_lr_flavour_4q, event.qg_lr_flavour_1q)
        event.qg_LR_flavour_4q_2q =  lratio(event.qg_lr_flavour_4q, event.qg_lr_flavour_2q)
        event.qg_LR_flavour_4q_3q =  lratio(event.qg_lr_flavour_4q, event.qg_lr_flavour_3q)

        event.qg_LR_flavour_4q_0q_1q =  lratio2(event.qg_lr_flavour_4q, event.qg_lr_flavour_0q, event.qg_lr_flavour_1q)
        event.qg_LR_flavour_4q_1q_2q =  lratio2(event.qg_lr_flavour_4q, event.qg_lr_flavour_1q, event.qg_lr_flavour_2q)
        event.qg_LR_flavour_4q_2q_3q =  lratio2(event.qg_lr_flavour_4q, event.qg_lr_flavour_2q, event.qg_lr_flavour_3q)

        event.qg_LR_flavour_4q_0q_1q_2q =  lratio3(event.qg_lr_flavour_4q, event.qg_lr_flavour_0q, event.qg_lr_flavour_1q, event.qg_lr_flavour_2q)
        event.qg_LR_flavour_4q_1q_2q_3q =  lratio3(event.qg_lr_flavour_4q, event.qg_lr_flavour_1q, event.qg_lr_flavour_2q, event.qg_lr_flavour_3q)

        event.qg_LR_flavour_4q_0q_1q_2q_3q =  lratio4(event.qg_lr_flavour_4q, event.qg_lr_flavour_0q, event.qg_lr_flavour_1q, event.qg_lr_flavour_2q, event.qg_lr_flavour_3q)

        
        event.passes_qgl = True
        return event
