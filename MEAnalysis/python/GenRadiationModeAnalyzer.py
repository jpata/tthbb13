from TTH.MEAnalysis.VHbbTree import lvec
from TTH.MEAnalysis.Analyzer import FilterAnalyzer
class GenRadiationModeAnalyzer(FilterAnalyzer):
    """
    Performs B/C counting in order to classify heavy flavour / light flavour events.

    We count the number of reconstructed jets which are matched to b/c quarks by CMSSW (ghost clustering).
    From this, the jets matched to b quarks from tops are subtracted.

    Therefore, nMatchSimB == 2 corresponds to 2 additional gluon radiation b quarks
    which are reconstructed as good jets.
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(GenRadiationModeAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(GenRadiationModeAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.counters["processing"].inc("processed")

        event.nMatchSimB = 0
        event.nMatchSimC = 0
        lv_bs = map(lvec, event.GenBQuarkFromTop)
        for jet in event.good_jets:
            lv_j = lvec(jet)

            if (lv_j.Pt() > 20 and abs(lv_j.Eta()) < 2.5):
                if any([lv_b.DeltaR(lv_j) < 0.5 for lv_b in lv_bs]):
                    continue
                absid = abs(jet.mcFlavour)
                if absid == 5:
                    event.nMatchSimB += 1
                if absid == 4:
                    event.nMatchSimC += 1

        passes = True
        if passes:
            self.counters["processing"].inc("passes")
        return passes

