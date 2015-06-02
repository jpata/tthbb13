from TTH.MEAnalysis.Analyzer import FilterAnalyzer
class SubjetAnalyzer(FilterAnalyzer):
    """
    TODO
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(SubjetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(SubjetAnalyzer, self).beginLoop(setup)

    def process(self, event):
        setattr( event, 'AfterSubjetAnalyzer', True )
        print 'In SubjetAnalyzer! event.AfterSubjetAnalyzer = {0}'.format(
            event.AfterSubjetAnalyzer )
