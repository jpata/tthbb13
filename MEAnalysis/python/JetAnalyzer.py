from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.VHbbTree import *
from TTH.MEAnalysis.vhbb_utils import *
from copy import deepcopy
import numpy as np
import copy

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
    jet.tf_b.SetNpx(10000)
    jet.tf_b.SetRange(0, 500)

    jet.tf_l.SetNpx(10000)
    jet.tf_l.SetRange(0, 500)

class JetAnalyzer(FilterAnalyzer):
    """
    Performs jet selection and b-tag counting.
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(JetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf

    def variateJets(self, jets, systematic, sigma):
        if systematic == "JES":
            newjets = deepcopy(jets)
            for i in range(len(jets)):
                if sigma > 0:
                    cf = sigma * newjets[i].corr_JECUp / newjets[i].corr

                elif sigma < 0:
                    cf = abs(sigma) * newjets[i].corr_JECDown / newjets[i].corr
                
                #get the uncorrected jets
                elif sigma == 0:
                    cf = 1.0 / newjets[i].corr

                newjets[i].pt *= cf
                newjets[i].mass *= cf
        return newjets

    def process(self, event):
        #pt-descending input jets
        if "input" in self.conf.general["verbosity"]:
            print "jets"
            for j in event.Jet:
                print "InJetReco", j.pt, j.eta, j.phi, j.mass, j.btagCSV, j.mcFlavour
                print "InJetGen", j.mcPt, j.mcEta, j.mcPhi, j.mcM

        event.MET = MET(pt=event.met.pt, phi=event.met.phi)
        event.MET_gen = MET(pt=event.MET.genPt, phi=event.MET.genPhi)
        event.MET_tt = MET(px=0, py=0)
        
        jets_raw = self.variateJets(event.Jet, "JES", 0)
        jets_JES_Up = self.variateJets(event.Jet, "JES", 1)
        jets_JES_Down = self.variateJets(event.Jet, "JES", -1)
        evdict = {}
        for name, jets in [
                ("raw", jets_raw),
                ("JESUp", jets_JES_Up),
                ("JESDown", jets_JES_Down)
            ]:
            if not name in self.conf.general["systematics"]:
                continue

            ev = FakeEvent(event)
            ev.Jet = jets
            ev.systematic = name
            evdict[name] = ev
        if "nominal" in self.conf.general["systematics"]:
            evdict["nominal"] = FakeEvent(event)
            evdict["nominal"].systematic = "nominal"

        for syst, event_syst in evdict.items():
            res = self._process(event_syst)
            evdict[syst] = res
        event.systResults = evdict

        return np.any([v.passes_jet for v in event.systResults.values()])

    def _process(self, event):
        pt_cut  = "pt"
        eta_cut = "eta"
        if event.is_sl:
            pt_cut  = "pt_sl"
            eta_cut = "eta_sl"
        if event.is_dl:
            pt_cut  = "pt_dl"
            eta_cut = "eta_dl"

        event.good_jets = sorted(
            filter(
                lambda x: (
                    x.pt > self.conf.jets[ pt_cut ]
                    and abs(x.eta) < self.conf.jets[ eta_cut ]
                    and x.neHEF < 0.99
                    and x.chEmEF < 0.99
                    and x.neEmEF < 0.99
                    and x.numberOfDaughters > 1
                    and x.chHEF > 0.0
                    and x.chMult > 0.0
                ), event.Jet
            ),
            key=lambda x: x.pt, reverse=True
        )


        if "debug" in self.conf.general["verbosity"]:
            print "All jets: ", len(event.Jet)
            for x in event.Jet:
                print "\t(%s, %s, neHEF=%s, chEmEF=%s, neEmEF=%s, nod=%s, chHEF=%s, chMult=%s, csv=%s)" % (x.pt, x.eta, x.neHEF, x.chEmEF, x.neEmEF, x.numberOfDaughters, x.chHEF, x.chMult, x.btagCSV)
            print "Good jets: ", len(event.good_jets)
            for x in event.good_jets:
                print "\t(%s, %s, neHEF=%s, chEmEF=%s, neEmEF=%s, nod=%s, chHEF=%s, chMult=%s, csv=%s)" % (x.pt, x.eta, x.neHEF, x.chEmEF, x.neEmEF, x.numberOfDaughters, x.chHEF, x.chMult, x.btagCSV)

        #Assing jet transfer functions
        for jet in event.good_jets:
            attach_jet_transfer_function(jet, self.conf)

        event.numJets = len(event.good_jets)

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
            setattr(event, "nB"+btag_wp_name, len(event.btagged_jets_bdisc[btag_wp_name]))

        #Find jets that pass/fail the specified default b-tagging algo/working point
        event.buntagged_jets_bdisc = event.buntagged_jets_bdisc[self.conf.jets["btagWP"]]
        event.btagged_jets_bdisc = event.btagged_jets_bdisc[self.conf.jets["btagWP"]]

        #Find how many of these tagged jets are actually true b jets
        event.n_tagwp_tagged_true_bjets = 0
        for j in event.btagged_jets_bdisc:
            if abs(j.mcFlavour) == 5:
                event.n_tagwp_tagged_true_bjets += 1

        #Require at least 3 (if is_sl) or 2 (is_dl) good jets in order to continue analysis
        passes = True
        if event.is_sl and len(event.good_jets) < 3:
            passes = False
        if event.is_dl:
            if len(event.good_jets) < 2:
                passes = False
            if len(event.good_jets) >=2:
                if event.good_jets[0].pt<self.conf.jets["pt"] or event.good_jets[1].pt<self.conf.jets["pt"]:
                    passes = False
        if event.is_fh:
            if len(event.good_jets) < 6:      
                passes = False        
            if len(event.good_jets) >=6:
                if event.good_jets[5].pt<self.conf.jets["pt_fh"]:
                    passes = False

        corrMet_px = event.MET.px
        corrMet_py = event.MET.py
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
        event.MET_jetcorr = MET(px=corrMet_px, py=corrMet_py)
        event.passes_jet = passes
        return event
