import logging
from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
from TTH.MEAnalysis.vhbb_utils import lvec
import ROOT

class FilterAnalyzer(Analyzer):
    """
    A generic analyzer that may filter events.
    Counts events the number of processed and passing events.
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(FilterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.logger = logging.getLogger(self.name)
        level = getattr(logging, self.conf.general["loglevel"].get(self.name, "WARNING"))
        self.logger.setLevel(level)
        print "logger {0} level {1}".format(self.name, level)

    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)


class CounterAnalyzer(FilterAnalyzer):
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(CounterAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
    
    def beginLoop(self, setup):
        super(CounterAnalyzer, self).beginLoop(setup)
        self.chist = ROOT.TH1F("CounterAnalyzer_count", "count", 1,0,1)
    
    def process(self, event):
        #super(CounterAnalyzer, self).process(event)
        self.chist.Fill(0)

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

        passes = True
        if not self.event_whitelist is None:
            passes = False
            if (event.input.run, event.input.lumi, event.input.evt) in self.event_whitelist:
                print "IDFilter", (event.input.run, event.input.lumi, event.input.evt)
                passes = True

        self.logger.info("starting EVENT run:lumi:event = {0}:{1}:{2}".format(
            event.input.run, event.input.lumi, event.input.evt
        ))
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
        event.weight_xs = self.xs/float(self.n_gen) if self.n_gen > 0 else 1
       

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
