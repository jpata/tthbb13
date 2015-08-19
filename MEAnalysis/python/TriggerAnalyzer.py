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
        
        for name in self.conf.trigger["HLTpaths"]:
            bit = getattr(event.input, name, 0)
            #print name, bit
            if (bit == 1): 
                event.triggerDecision = True
        
        passes = False
        if (event.triggerDecision):
            passes = True
        if (not self.conf.trigger["filter"] ):
            passes = True
        
        return True
