from TTH.MEAnalysis.Analyzer import FilterAnalyzer

class TreeVarAnalyzer(FilterAnalyzer):
    """
    """

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TreeVarAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def process(self, event):
       

        setattr( event, 'boosted_bjets', [] )
        setattr( event, 'boosted_ljets', [] )
        setattr( event, 'topCandidate', [] )
        setattr( event, 'othertopCandidate', [] )
        setattr( event, 'higgsCandidate', [] )
        for syst, event_syst in event.systResults.items():
            event_syst.mem_results_tth = getattr(event_syst, "mem_results_tth", [])
            event_syst.mem_results_ttbb = getattr(event_syst, "mem_results_ttbb", [])
            event_syst.fw_h_alljets = getattr(event_syst, "fw_h_alljets", [])
            event_syst.fw_h_btagjets = getattr(event_syst, "fw_h_btagjets", [])
            event_syst.fw_h_untagjets = getattr(event_syst, "fw_h_untagjets", [])
            
            for k, v in event_syst.__dict__.items():
                event.__dict__[k + "_" + syst] = v
        
            #for k, v in event_syst.__dict__.items():
            #    print syst, k, v 
        #for k, v in event.__dict__.items():
        #    print "Event", k, v 
        
        for br in ["boosted_bjets", "boosted_ljets", "topCandidate", "othertopCandidate", "higgsCandidate"]:
            if not hasattr(event, br+"_nominal"):
                setattr(event, br + "_nominal", [])

        return True
