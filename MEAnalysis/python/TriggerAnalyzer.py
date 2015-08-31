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
        for name in self.conf.trigger["HLTpaths"]:
            bit = int(getattr(event.input, name, 0))
            event.trigvec += [bit == 1]
            #print name, bit
            if (bit == 1):
                event.triggerDecision = True
                if "trigger" in self.conf.general["verbosity"]:
                    print "[trigger]", name, bit
        event.triggerBitmask = int(sum(1<<i for i, b in enumerate(event.trigvec) if b))
        if "trigger" in self.conf.general["verbosity"]:
            print "[trigger] bitmask", event.triggerBitmask
        passes = True
        if self.conf.trigger["filter"] and not event.triggerDecision:
            passes = False
        
        return passes
