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
        self.qglplots_flavour = ROOT.TFile(self.conf.general["QGLPlotsFile_flavour"])
      
        self.qgl_flavour_pdfs = {
        }
        for x in ["q","g"]:
            if (x=="q"):
                self.qgl_flavour_pdfs[x] = self.qglplots_flavour.Get(
                    "histo3D_quark"
                )
            else:
                self.qgl_flavour_pdfs[x] = self.qglplots_flavour.Get(
                    "histo3D_gluon"
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
            nb = h.FindBin(qgl,pt,eta)
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
             
            maxj = 10
            if (len(probs)<10):
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
        toDo =  self.conf.general["QGLtoDo"]
        if len(toDo)==0:
            return event
        
        toDo = {
            #nB:[(nQ1,nQ2),...] = test the hypothesis nQ1 quarks vs nQ2 quarks, given nB b-quarks (that are removed from the quarks/gluon likelihood computing).
            3:[(3,0),(3,2),(4,0),(4,3),(5,4)], 
            4:[(3,0),(3,2),(4,0),(4,3)]
        }
        
        maxLikelihood_perm = {}
        maxLikelihood = {}
        for nB in toDo:
            jets_for_qg_lr =  getattr(event,"buntagged_jets_maxLikelihood_%sb"%nB)[:]
            jet_probs = {
                kind: [
                    self.evaluate_jet_prob(j.pt, j.eta, j.qgl, kind)
                    for j in jets_for_qg_lr
                ]
                for kind in [
                    "flavour"
                ]
            }
            allQ = set()
            for (nQ1,nQ2) in toDo[nB]:
                allQ.add(nQ1)
                allQ.add(nQ2)
            for nQ in allQ:
                maxLikelihood[(nB,nQ)], maxLikelihood_perm[(nB,nQ)] = self.qg_likelihood(jet_probs["flavour"], min(len(jets_for_qg_lr),nQ))
                
        
        def lratio(l1, l2):
            if l1+l2>0:
                return l1/(l1+l2)
            else:
                return 0.0
        
        for nB in toDo:
            for (nQ1,nQ2) in toDo[nB]:
                setattr(event,"qg_LR_%sb_flavour_%sq_%sq"%(nB,nQ1,nQ2),lratio(maxLikelihood[(nB,nQ1)],maxLikelihood[(nB,nQ2)]))
        
        event.passes_qgl = True
        return event
