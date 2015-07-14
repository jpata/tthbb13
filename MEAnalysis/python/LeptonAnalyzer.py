from TTH.MEAnalysis.Analyzer import FilterAnalyzer
class LeptonAnalyzer(FilterAnalyzer):
    """
    Analyzes leptons and applies single-lepton and di-lepton selection.

    Relies on TTH.MEAnalysis.VHbbTree.EventAnalyzer for inputs.

    Configuration:
    Conf.leptons[channel][cuttype] where channel=mu,ele, cuttype=tight,loose,(+veto)
    the lepton cuts must specify pt, eta and isolation cuts.

    Returns:
    event.good_leptons (list of VHbbTree.selLeptons): contains the leptons that pass the SL XOR DL selection.
        Leptons are ordered by flavour and pt.
    event.is_sl, is_dl (bool): specifies if the event passes SL or DL selection.

    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(LeptonAnalyzer, self).beginLoop(setup)

    def process(self, event):

        event.mu = filter(
            lambda x: abs(x.pdgId) == 13,
            event.selLeptons,
        )
        if "debug" in self.conf.general["verbosity"]:
            for it in event.mu:
                print "input muons"
                print it
                (self.conf.leptons["mu"]["debug"])(it)

        event.el = filter(
            lambda x: abs(x.pdgId) == 11,
            event.selLeptons,
        )
        if "debug" in self.conf.general["verbosity"]:
            print "input electrons"
            for it in event.el:
                print it
                (self.conf.leptons["el"]["debug"])(it)
    
        #for SL = tight
        #event.mu_tight <= SL signal muon
        #event.el_tight <= SL signal ele
        #event.mu_tight_veto <= SL veto muon, NOT in mu_tight
        #event.el_tight_veto <= SL veto ele, NOT in el_tight
       
        #DL = loose
        #event.mu_loose <= DL signal muon
        #event.el_loose <= DL signal ele
        #event.mu_loose_veto <= DL veto muon, NOT in mu_loose
        #event.el_loose_veto <= DL veto ele, NOT in el_loose

        for a in ["tight", "loose"]:
            for b in ["", "_veto"]:
                sumleps = []
                for l in ["mu", "el"]:
                    if "debug" in self.conf.general["verbosity"]:
                        print a,b,l
                    lepcuts = self.conf.leptons[l][a+b]
                    incoll = getattr(event, l)

                    isotype = self.conf.leptons[l]["isotype"]
                    isocut = lepcuts.get("iso", 99)
                    leps = filter(
                        lambda x: (
                            x.pt > lepcuts["pt"]
                            and abs(x.eta) < lepcuts["eta"]
                            #if specified, apply an additional isolation cut
                            and abs(getattr(x, isotype)) < isocut
                        ), incoll
                    )
                    leps = filter(lepcuts["idcut"], leps)
                    leps = sorted(leps, key=lambda x: x.pt, reverse=True)

                    #veto leptons are defined to pass the veto lepton cuts and fail the signal lepton cuts
                    if b == "_veto":
                        #take the signal leptons (not veto)
                        good = getattr(event, "{0}_{1}".format(l, a))
                        #veto = veto_cuts && !(signal)
                        leps = filter(lambda x: x not in good, leps)
                    if "debug" in self.conf.general["verbosity"]:
                        for it in leps:
                            (self.conf.leptons[l]["debug"])(it)

                    sumleps += leps
                    lt = l + "_" + a + b
                    setattr(event, lt, leps)
                    setattr(event, "n_"+lt, len(leps))

                setattr(event, "lep_{0}".format(a+b), sumleps)
                setattr(event, "n_lep_{0}".format(a+b), len(sumleps))

        if "debug" in self.conf.general["verbosity"]:
            print "n_lep_tight=%s, n_lep_loose=%s, n_lep_tight_veto=%s, n_lep_loose_veto=%s" % (event.n_lep_tight, event.n_lep_loose, event.n_lep_tight_veto, event.n_lep_loose_veto)

        event.is_sl = (event.n_lep_tight == 1 and event.n_lep_tight_veto == 0)
        event.is_dl = (event.n_lep_loose == 2 and event.n_lep_loose_veto == 0)

        if event.is_sl:
            event.good_leptons = event.mu_tight + event.el_tight
            event.veto_leptons = event.mu_tight_veto + event.el_tight_veto
        if event.is_dl:
            event.good_leptons = event.mu_loose + event.el_loose
            event.veto_leptons = event.mu_loose_veto + event.el_loose_veto

        passes = event.is_sl or event.is_dl
        if event.is_sl and event.is_dl:
            print "DEBUG: The event (%s,%s,%s) is both sl and dl" % (event.input.run,event.input.lumi,event.input.evt)
            passes = False

        return passes
