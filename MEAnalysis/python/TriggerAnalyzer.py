from PhysicsTools.HeppyCore.framework.analyzer import Analyzer
from TTH.MEAnalysis.vhbb_utils import lvec
from TTH.MEAnalysis.Analyzer import FilterAnalyzer

class TriggerAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TriggerAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(TriggerAnalyzer, self).beginLoop(setup)

    def process(self, event):

        event.triggerDecision = False
        event.trigvec = []
        if self.cfg_comp.isMC:
            triglist = self.conf.trigger["trigTable"]
        else:
            triglist = self.conf.trigger["trigTableData"]

        for pathname, trigs in triglist.items():
            for name in trigs:
                bit = int(getattr(event.input, name, -1))
                setattr(event, name, bit)
                event.trigvec += [bit == 1]
                #print name, bit
                if "trigger" in self.conf.general["verbosity"]:
                    print "[trigger]", name, bit
                if (bit == 1):
                    event.triggerDecision = True

        #event.triggerBitmask = int(sum(1<<i for i, b in enumerate(event.trigvec) if b))
        #if "trigger" in self.conf.general["verbosity"]:
        #    print "[trigger] bitmask", event.triggerBitmask
        #passes = True
        #if self.conf.trigger["filter"] and not event.triggerDecision:
        #    passes = False
        
        return self.conf.general["passall"] or passes
