from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
from TTH.MEAnalysis.vhbb_utils import lvec

class FilterAnalyzer(Analyzer):
    """
    A generic analyzer that may filter events.
    Counts events the number of processed and passing events.
    """
    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)
        self.counters.addCounter("processing")
        self.counters["processing"].register("processed")
        self.counters["processing"].register("passes")

class EventIDFilterAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventIDFilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.event_whitelist = self.conf.general.get("eventWhitelist", None)

    def beginLoop(self, setup):
        super(EventIDFilterAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.counters["processing"].inc("processed")

        passes = True
        if not self.event_whitelist is None:
            passes = False
            if (event.input.run, event.input.lumi, event.input.evt) in self.event_whitelist:
                print "IDFilter", (event.input.run, event.input.lumi, event.input.evt)
                passes = True

        if passes and "eventboundary" in self.conf.general["verbosity"]:
            print "---starting EVENT r:l:e", event.input.run, event.input.lumi, event.input.evt
        if passes:
            self.counters["processing"].inc("passes")
        return passes


class EventWeightAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EventWeightAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.n_gen = cfg_comp.n_gen
        self.xs = cfg_comp.xs

    def beginLoop(self, setup):
        super(EventWeightAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.counters["processing"].inc("processed")
        print "xsec ", self.xs
        print "ngen ", self.n_gen
        event.weight_xs = self.xs/float(self.n_gen)
        print "weight ", event.weight_xs

        return True

class PrimaryVertexAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(PrimaryVertexAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(PrimaryVertexAnalyzer, self).beginLoop(setup)

    def process(self, event):
        pvs = event.primaryVertices
        if len(pvs) > 0:
            event.primaryVertex = pvs[0]
            event.passPV = (not event.primaryVertex.isFake) and (event.primaryVertex.ndof >= 4 and event.primaryVertex.Rho <= 2)
        else:
            event.passPV = False
            print "PrimaryVertexAnalyzer: number of vertices=", (len(pvs))
            return False
        return True
