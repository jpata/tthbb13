from TTH.MEAnalysis.VHbbTree import lvec
import ROOT
import copy
ROOT.gSystem.Load("libCintex")
ROOT.gROOT.ProcessLine('ROOT::Cintex::Cintex::Enable();')
ROOT.gSystem.Load("libTTHMEAnalysis")

from TTH.MEAnalysis.Analyzer import FilterAnalyzer

CvectorTLorentzVector = getattr(ROOT, "std::vector<TLorentzVector>")
EventShapeVariables = getattr(ROOT, "EventShapeVariables")

class MVAVarAnalyzer(FilterAnalyzer):
    """
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(MVAVarAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(MVAVarAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.counters["processing"].inc("processed")
        vecs = CvectorTLorentzVector()
        for jet in event.good_jets:
            vecs.push_back(lvec(jet))
        evshape = EventShapeVariables(vecs)
        eigs = evshape.compEigenValues(2.0)
        print "isotropy", evshape.isotropy()
        print "eigs", eigs[0], eigs[1], eigs[2]
