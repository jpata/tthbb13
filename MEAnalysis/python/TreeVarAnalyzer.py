from TTH.MEAnalysis.Analyzer import FilterAnalyzer

class TreeVarAnalyzer(FilterAnalyzer):
    """
    Flattens the systematic dictionary into the event.
    {"JESUp": res} => event.res_JESUp
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TreeVarAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def process(self, event):
        setattr( event, 'boosted_bjets', [] )
        setattr( event, 'boosted_ljets', [] )
        setattr( event, 'topCandidate', [] )
        setattr( event, 'othertopCandidate', [])
        setattr( event, 'topCandidatesSync', [])    
        setattr( event, 'higgsCandidate', [] )
        
        #FIXME: currently, gen-level analysis is redone for systematic variations
        #in order to correctly ntuplize, we need to define event.genTopLep = event.systResults["nominal"].genTopLep etc
        event.genTopLep = getattr(event.systResults["nominal"], "genTopLep", [])
        event.genTopHad = getattr(event.systResults["nominal"], "genTopHad", [])
        
        for syst, event_syst in event.systResults.items():
            event_syst.common_mem = getattr(event_syst, "common_mem", [])
            event_syst.common_bdt = getattr(event_syst, "common_bdt", -1)
            event_syst.fw_h_alljets = getattr(event_syst, "fw_h_alljets", [])
            event_syst.fw_h_btagjets = getattr(event_syst, "fw_h_btagjets", [])
            event_syst.fw_h_untagjets = getattr(event_syst, "fw_h_untagjets", [])
            
            #add all variated quantities to event with a suffix
            for k, v in event_syst.__dict__.items():
                event.__dict__[k + "_" + syst] = v
        
        for br in ["boosted_bjets", "boosted_ljets", "topCandidate", "othertopCandidate", "topCandidatesSync", "higgsCandidate"]:
            if not hasattr(event, br+"_nominal"):
                setattr(event, br + "_nominal", [])
        return True
