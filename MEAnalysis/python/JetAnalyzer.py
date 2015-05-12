from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.VHbbTree import *

def attach_jet_transfer_function(jet, conf, eval_gen=False):
    """
    Attaches transfer functions to the supplied jet based on the jet eta bin.

    eval_gen:specifies how the transfer functions are interpreted
        If True, TF [0] - reco, x - gen
        If False, TF [0] - gen, x - reco
    """
    jet_eta_bin = 0
    if abs(jet.eta)>1.0:
        jet_eta_bin = 1
    jet.tf_b = conf.tf_matrix['b'][jet_eta_bin].Make_Formula(eval_gen)
    jet.tf_l = conf.tf_matrix['l'][jet_eta_bin].Make_Formula(eval_gen)

class JetAnalyzer(FilterAnalyzer):
    """
    Performs jet selection and b-tag counting.
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(JetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def beginLoop(self, setup):
        super(JetAnalyzer, self).beginLoop(setup)
        self.counters.addCounter("jets")
        self.counters["jets"].register("any")
        self.counters["jets"].register("good")
        for (btag_wp_name, btag_wp) in self.conf.jets["btagWPs"].items():
            self.counters["jets"].register(btag_wp_name)


    def process(self, event):
        self.counters["processing"].inc("processed")
        self.counters["jets"].inc("any", len(event.Jet))

        #pt-descending input jets
        if "input" in self.conf.general["verbosity"]:
            print "jets"
            for j in event.Jet:
                print "ijet", j.pt, j.eta, j.phi, j.mass, j.btagCSV, j.mcFlavour

        event.good_jets = sorted(
            filter(
                lambda x: (
                    x.pt > self.conf.jets["pt"]
                    and abs(x.eta) < self.conf.jets["eta"]
                ), event.Jet
            ),
            key=lambda x: x.pt, reverse=True
        )


        #Assing jet transfer functions
        for jet in event.good_jets:
            attach_jet_transfer_function(jet, self.conf)

        event.numJets = len(event.good_jets)
        self.counters["jets"].inc("good", len(event.good_jets))

        event.btagged_jets_bdisc = {}
        event.buntagged_jets_bdisc = {}
        for (btag_wp_name, btag_wp) in self.conf.jets["btagWPs"].items():
            algo, wp = btag_wp
            event.btagged_jets_bdisc[btag_wp_name] = filter(
                lambda x: getattr(x, algo) > wp,
                event.good_jets
            )
            event.buntagged_jets_bdisc[btag_wp_name] = filter(
                lambda x: getattr(x, algo) <= wp,
                event.good_jets
            )
            self.counters["jets"].inc(btag_wp_name,
                len(event.btagged_jets_bdisc[btag_wp_name])
            )
            setattr(event, "nB"+btag_wp_name, len(event.btagged_jets_bdisc[btag_wp_name]))

        #Find jets that pass/fail the specified default b-tagging algo/working point
        event.buntagged_jets_bdisc = event.buntagged_jets_bdisc[self.conf.jets["btagWP"]]
        event.btagged_jets_bdisc = event.btagged_jets_bdisc[self.conf.jets["btagWP"]]

        #Find how many of these tagged jets are actually true b jets
        event.n_tagwp_tagged_true_bjets = 0
        for j in event.btagged_jets_bdisc:
            if abs(j.mcFlavour) == 5:
                event.n_tagwp_tagged_true_bjets += 1

        #Require at least 4 good jets in order to continue analysis
        passes = len(event.good_jets) >= 4
        if passes:
            self.counters["processing"].inc("passes")

        corrMet_px = event.met[0].px
        corrMet_py = event.met[0].py
        sum_dEx = 0
        sum_dEy = 0
        for jet in event.good_jets:
            Prec = lvec(jet)
            Pgen = lvec(jet)
            Pgen.SetPtEtaPhiM(jet.mcPt, jet.mcEta, jet.mcPhi, jet.mcM)
            Erec = Prec.E()
            Egen = Pgen.E()
            dEx = (Erec-Egen) * Prec.Px()/Prec.P()
            dEy = (Erec-Egen) * Prec.Py()/Prec.P()
            #print Erec, Egen
            sum_dEx += dEx
            sum_dEy += dEy
        corrMet_px += sum_dEx
        corrMet_py += sum_dEy
        #print (sum_dEx, sum_dEy), (corrMet_px, event.met[0].px), (corrMet_py, event.met[0].py)
        event.met_jetcorr = [MET(px=corrMet_px, py=corrMet_py)]
        event.met_gen = [MET(pt=event.met[0].genPt, phi=event.met[0].genPhi)]

        return passes
