from TTH.MEAnalysis.Analyzer import FilterAnalyzer
import ROOT
from TTH.MEAnalysis.vhbb_utils import lvec

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
            print "input muons: ", len(event.mu)
            for it in event.mu:
                (self.conf.leptons["mu"]["debug"])(it)

        event.el = filter(
            lambda x: abs(x.pdgId) == 11,
            event.selLeptons,
        )
        if "debug" in self.conf.general["verbosity"]:
            print "input electrons: ", len(event.el)
            for it in event.el:
                (self.conf.leptons["el"]["debug"])(it)

        for id_type in ["SL", "DL", "veto"]:
            sumleps = []
            for lep_flavour in ["mu", "el"]:
                lepcuts = self.conf.leptons[lep_flavour][id_type]
                incoll = getattr(event, lep_flavour)
                
                
                isotype = self.conf.leptons[lep_flavour]["isotype"]
                isocut = lepcuts.get("iso", 99)
                leps = filter(
                    lambda x, lepcuts=lepcuts: (
                        x.pt > lepcuts.get("pt", 0)
                        and abs(x.eta) < lepcuts["eta"]
                    ), incoll
                )
                #Apply isolation cut
                if isotype != "none":
                    leps = filter(
                        lambda x, isotype=isotype, isocut=isocut: abs(getattr(x, isotype)) < isocut, leps
                    )
                leps = sorted(leps, key=lambda x: x.pt, reverse=True)
                leps = filter(lepcuts["idcut"], leps)

                #if defined additional pt cuts in DL
                newleps = [] 
                c0 = lepcuts.get("pt_leading", 0)
                c1 = lepcuts.get("pt_subleading", 0)
                for ilep, lep in enumerate(leps):
                    if len(newleps) == 0:
                        cut = c0
                    else:
                        cut = c1
                    if lep.pt > cut: 
                        newleps += [lep]
                leps = newleps

                sumleps += leps
                lepname = lep_flavour + "_" + id_type
                setattr(event, lepname, leps)
                setattr(event, "n_"+  lepname, len(leps))

                setattr(event, "lep_{0}".format(id_type), sumleps)
                setattr(event, "n_lep_{0}".format(id_type), len(sumleps))

        if "debug" in self.conf.general["verbosity"]:
            print "SL mu"
            for l in event.mu_SL:
                (self.conf.leptons["mu"]["debug"])(l)
            print "DL mu"
            for l in event.mu_DL:
                (self.conf.leptons["mu"]["debug"])(l)
            print "SL el"
            for l in event.el_SL:
                (self.conf.leptons["el"]["debug"])(l)
            print "DL el"
            for l in event.el_DL:
                (self.conf.leptons["el"]["debug"])(l)
            print "veto mu"
            for l in event.mu_veto:
                (self.conf.leptons["mu"]["debug"])(l)
            print "veto el"
            for l in event.el_veto:
                (self.conf.leptons["el"]["debug"])(l)

            print "n_lep_tight={0}, n_lep_loose={1}, n_lep_tight_veto={2}".format(event.n_lep_SL, event.n_lep_DL, event.n_lep_veto)

        event.is_sl = (event.n_lep_SL == 1 and event.n_lep_veto == 1)
        event.is_dl = (event.n_lep_DL == 2 and event.n_lep_veto == 2)
        event.is_fh = (not event.is_sl and not event.is_dl)
        if "debug" in self.conf.general["verbosity"]:
            print "DEBUG: is_sl, is_dl, is_fh", event.is_sl, event.is_dl, event.is_fh
        
        #Calculate di-lepton system momentum
        event.dilepton_p4 = ROOT.TLorentzVector()
        if event.is_sl:
            event.good_leptons = event.lep_SL
            event.veto_leptons = event.lep_veto
        elif event.is_dl:
            event.good_leptons =event.lep_DL
            event.veto_leptons = event.lep_veto
            for lv in [lvec(l) for l in event.good_leptons]:
                event.dilepton_p4 += lv
        elif event.is_fh:
            event.good_leptons = []
            event.veto_leptons = []
        
        event.good_leptons = sorted(event.good_leptons, key=lambda x: x.pt, reverse=True)
        event.veto_leptons = sorted(event.veto_leptons, key=lambda x: x.pt, reverse=True)

        #apply configuration-dependent selection
        passes = self.conf.leptons["selection"](event)
        if "debug" in self.conf.general["verbosity"]:
            print "LeptonAnalyzer selection", passes
        if event.is_sl and event.is_dl:
            print "DEBUG: The event (%s,%s,%s) is both sl and dl" % (event.input.run,event.input.lumi,event.input.evt)
            print "SL mu"
            for lep in event.mu_SL:
                (self.conf.leptons["mu"]["debug"])(lep)
            print "DL mu"
            for lep in event.mu_DL:
                (self.conf.leptons["mu"]["debug"])(lep)
                
            print "SL el"
            for lep in event.el_SL:
                (self.conf.leptons["el"]["debug"])(lep)
            print "DL el"
            for lep in event.el_DL:
                (self.conf.leptons["el"]["debug"])(lep)
                
            print "veto mu"
            for lep in event.mu_veto:
                (self.conf.leptons["mu"]["debug"])(lep)
            print "veto el"
            for lep in event.mu_veto:
                (self.conf.leptons["el"]["debug"])(lep)
            passes = False
            print "WARNING: Overlapping event"

        return self.conf.general["passall"] or passes
