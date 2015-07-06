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

        self.counters["processing"].register("sl")
        self.counters["processing"].register("dl")
        self.counters["processing"].register("slanddl")

        self.counters.addCounter("leptons")
        self.counters["leptons"].register("any")
        for l in ["mu", "el"]:
            for a in ["tight", "loose"]:
                for b in ["", "_veto"]:
                    lt = l + "_" + a + b
                    self.counters["leptons"].register(lt)

    def process(self, event):
        self.counters["processing"].inc("processed")
        self.counters["leptons"].inc("any", len(event.selLeptons))

        event.mu = filter(
            lambda x: abs(x.pdgId) == 13,
            event.selLeptons,
        )
        event.el = filter(
            lambda x: abs(x.pdgId) == 11,
            event.selLeptons,
        )

        for a in ["tight", "loose"]:
            for b in ["", "_veto"]:
                sumleps = []
                for l in ["mu", "el"]:
                    lepcuts = self.conf.leptons[l][a+b]
                    incoll = getattr(event, l)

                    if "debug" in self.conf.general["verbosity"]:
                        for it in incoll:
                            (self.conf.leptons[l]["debug"])(it)

                    leps = filter(
                        lambda x: (
                            x.pt > lepcuts["pt"]
                            and abs(x.eta) < lepcuts["eta"]
                            #if specified, apply an additional isolation cut
                            and abs(getattr(x, self.conf.leptons[l]["isotype"])) < lepcuts.get("iso", 99)
                        ), incoll
                    )

                    #remove veto leptons that also pass the good lepton cuts
                    if b == "_veto":
                        good = getattr(event, "{0}_{1}".format(l, a))
                        leps = filter(lambda x: x not in good, leps)

                    leps = filter(lepcuts["idcut"], leps)
                    leps = sorted(leps, key=lambda x: x.pt, reverse=True)
                    sumleps += leps
                    lt = l + "_" + a + b
                    setattr(event, lt, leps)
                    setattr(event, "n_"+lt, len(leps))
                    self.counters["leptons"].inc(lt, len(leps))

                setattr(event, "lep_{0}".format(a+b), sumleps)
                setattr(event, "n_lep_{0}".format(a+b), len(sumleps))

        if "debug" in self.conf.general["verbosity"]:
            print "n_lep_tight=%s, n_lep_loose=%s, n_lep_tight_veto=%s, n_lep_loose_veto=%s" % (event.n_lep_tight, event.n_lep_loose, event.n_lep_tight_veto, event.n_lep_loose_veto)

        event.is_sl = (event.n_lep_tight == 1 and event.n_lep_tight_veto == 0)
        event.is_dl = (event.n_lep_loose == 2 and event.n_lep_loose_veto == 0)

        if event.is_sl:
            self.counters["processing"].inc("sl")
            event.good_leptons = event.mu_tight + event.el_tight
        if event.is_dl:
            self.counters["processing"].inc("dl")
            event.good_leptons = event.mu_loose + event.el_loose

        passes = event.is_sl or event.is_dl
        if event.is_sl and event.is_dl:
            self.counters["processing"].inc("slanddl")            
            if "debug" in self.conf.general["verbosity"]:
                print "DEBUG: The event (%s,%s,%s) is both sl and dl" % (event.input.run,event.input.lumi,event.input.evt)
            passes = False

        if passes:
            self.counters["processing"].inc("passes")
        else:
            if "debug" in self.conf.general["verbosity"]:
                print "DEBUG: The event (%s,%s,%s) is neither sl nor dl" % (event.input.run,event.input.lumi,event.input.evt)

        return passes
