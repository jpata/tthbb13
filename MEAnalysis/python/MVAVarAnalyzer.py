from TTH.MEAnalysis.VHbbTree import lvec
import ROOT
import copy
import numpy as np
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
        event.momentum_eig0 = eigs[0]
        event.momentum_eig1 = eigs[1]
        event.momentum_eig2 = eigs[2]

        event.isotropy = evshape.isotropy()
        event.sphericity = evshape.sphericity(eigs)
        event.aplanarity = evshape.aplanarity(eigs)
        event.C = evshape.D(eigs)
        event.D = evshape.D(eigs)

        event.mean_bdisc = np.mean([j.btagCSV for j in event.good_jets])
        event.mean_bdisc_btag = np.mean([j.btagCSV for j in event.selected_btagged_jets])
        event.std_bdisc = np.std([j.btagCSV for j in event.good_jets])
        event.std_bdisc_btag = np.std([j.btagCSV for j in event.selected_btagged_jets])
        drs = []
        for j1 in event.selected_btagged_jets:
            for j2 in event.selected_btagged_jets:
                if j1==j2:
                    continue
                l1 = lvec(j1)
                l2 = lvec(j2)
                drs += [l1.DeltaR(l2)]
        if len(drs)>0:
            event.min_dr_btag = np.min(drs)
            event.mean_dr_btag = np.mean(drs, -1)
            event.std_dr_btag = np.std(drs)
        else:
            event.min_dr_btag = -1.0
            event.mean_dr_btag = -1.0
            event.std_dr_btag = -1.0

        for i in range(min(4, len(event.selected_btagged_jets_high))):
            setattr(event, "jet_btag_{0}".format(i), event.selected_btagged_jets_high[i])

        event.ht = np.sum([j.pt for j in event.good_jets])
