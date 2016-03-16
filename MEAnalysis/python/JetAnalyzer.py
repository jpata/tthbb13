from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.VHbbTree import *
from TTH.MEAnalysis.vhbb_utils import *
from copy import deepcopy
import numpy as np
import copy


#FIXME: understand the effect of cropping the transfer functions
def attach_jet_transfer_function(jet, conf):
    """
    Attaches transfer functions to the supplied jet based on the jet eta bin.
    """
    jet_eta_bin = 0
    if abs(jet.eta)>1.0:
        jet_eta_bin = 1
    jet.tf_b = conf.tf_formula['b'][jet_eta_bin]
    jet.tf_l = conf.tf_formula['l'][jet_eta_bin]
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

    def beginLoop(self, setup):
        super(JetAnalyzer, self).beginLoop(setup)

    def variateJets(self, jets, systematic, sigma):
        newjets = deepcopy(jets)
        if self.cfg_comp.isMC and systematic == "JES":
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
        elif self.cfg_comp.isMC and systematic == "JER":
            for i in range(len(jets)):
                if newjets[i].corr_JER > 0:
                    if sigma > 0:
                        cf =  sigma * newjets[i].corr_JERUp / newjets[i].corr_JER
                    elif sigma < 0:
                        cf = abs(sigma) * newjets[i].corr_JERDown / newjets[i].corr_JER
                    
                    #get the uncorrected jets
                    elif sigma == 0:
                        cf = 1.0 / newjets[i].corr_JER
                else:
                    cf = 0.0

                newjets[i].pt *= cf
                newjets[i].mass *= cf
        return newjets

    def process(self, event):

        #FIXME: why discarded jets no longer in vhbb?
        #injets = event.Jet+event.DiscardedJet
        event.injets = event.Jet
        #pt-descending input jets
        if "input" in self.conf.general["verbosity"]:
            autolog("jets input") 
            for ij, j in enumerate(event.injets):
                autolog("InJetReco", ij, j.pt, j.eta, j.phi, j.mass, j.btagCSV, j.mcFlavour)
                autolog("InJetGen", ij, j.mcPt, j.mcEta, j.mcPhi, j.mcM)

        event.MET = MET(pt=event.met.pt, phi=event.met.phi)
        event.MET_gen = MET(pt=event.MET.genPt, phi=event.MET.genPhi)
        event.MET_tt = MET(px=0, py=0)
       
        evdict = {}
        if self.cfg_comp.isMC:
            jets_raw = self.variateJets(event.Jet, "JES", 0)
            jets_JES_Up = self.variateJets(event.Jet, "JES", 1)
            jets_JES_Down = self.variateJets(event.Jet, "JES", -1)
            jets_JER_Up = self.variateJets(event.Jet, "JER", 1)
            jets_JER_Down = self.variateJets(event.Jet, "JER", -1)
            for name, jets in [
                    ("raw", jets_raw),
                    ("JESUp", jets_JES_Up),
                    ("JESDown", jets_JES_Down),
                    ("JERUp", jets_JER_Up),
                    ("JERDown", jets_JER_Down)
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
            if "debug" in self.conf.general["verbosity"]:
                autolog("processing systematic", syst)
            res = self._process(event_syst)
            evdict[syst] = res
        event.systResults = evdict

        return self.conf.general["passall"] or np.any([v.passes_jet for v in event.systResults.values()])

    def _process(self, event):

        #choose pt cut key based on lepton channel
        pt_cut  = "pt"
        eta_cut = "eta"
        if event.is_sl:
            pt_cut  = "pt_sl"
            eta_cut = "eta_sl"
        elif event.is_dl:
            pt_cut  = "pt_dl"
            eta_cut = "eta_dl"
        
        #define lepton-channel specific selection function
        jetsel = lambda x, self=self: (
            x.pt > self.conf.jets[pt_cut]
            and abs(x.eta) < self.conf.jets[eta_cut]
            and self.conf.jets["selection"](x)
        )
        
        jetsel_loose_pt = lambda x, self=self: (
            x.pt > 20
            and abs(x.eta) < self.conf.jets[eta_cut]
            and self.conf.jets["selection"](x)
        )

        #Identify loose jets by (pt, eta)
        loose_jets = sorted(filter(
            jetsel_loose_pt, event.injets 
            ), key=lambda x: x.pt, reverse=True
        )

        #In DL, the leading two jets must pass the tighter pt cut,
        #whereas the trailing can pass the looser
        #if event.is_dl:
        #    good_jets_leading = filter(
        #        lambda x, self=self: x.pt > self.conf.jets["pt_sl"],
        #        event.good_jets[:2]
        #    )
        #    event.good_jets = good_jets_leading + event.good_jets[2:]


        #Take care of overlaps between jets and veto leptons
        jets_to_remove = []
        for lep in event.veto_leptons:
            #overlaps removed by delta R
            for jet in loose_jets:
                lv1 = lvec(jet)
                lv2 = lvec(lep)
                dr = lv1.DeltaR(lv2)
                if dr < 0.4:
                    if "jets" in self.conf.general["verbosity"] or "debug" in self.conf.general["verbosity"]:
                        autolog("[jet lepton cleaning] deltaR", dr, lep.pt, lep.eta, lep.phi, jet.pt, jet.eta, jet.phi)
                    jets_to_remove += [jet]

        #Now actually remove the overlapping jets
        for jet in jets_to_remove:
            if "jets" in self.conf.general["verbosity"] or "debug" in self.conf.general["verbosity"]:
                autolog("removing jet", jet.pt, jet.eta)
            if jet in loose_jets:
                loose_jets.remove(jet)
        
        #in DL apply two-stage pt cuts
        #Since this relies on jet counting, needs to be done **after** any other jet filtering
        if event.is_dl:
            good_jets_dl = []
            for jet in loose_jets:
                if len(good_jets_dl) < 2:
                    ptcut = self.conf.jets["pt_sl"]
                else:
                    ptcut = self.conf.jets["pt_dl"]
                if jet.pt > ptcut:
                    good_jets_dl += [jet]
            loose_jets = good_jets_dl

        #Now apply true pt cuts to identify analysis jets
        event.good_jets = filter(jetsel, loose_jets)
        event.loose_jets = filter(lambda x, event=event: x not in event.good_jets, loose_jets) 

        if "debug" in self.conf.general["verbosity"]:
            autolog("All jets: ", len(event.injets))
            for x in event.injets:
                autolog(str(x))
            autolog("Loose jets: ", len(event.loose_jets))
            for x in event.loose_jets:
                autolog(str(x))
            autolog("Good jets: ", len(event.good_jets))
            for x in event.good_jets:
                autolog(str(x))

        #Assing jet transfer functions
        for jet in event.loose_jets + event.good_jets:
            attach_jet_transfer_function(jet, self.conf)

        event.numJets = len(event.good_jets)

        event.btagged_jets_bdisc = {}
        event.buntagged_jets_bdisc = {}
        for (btag_wp_name, btag_wp) in self.conf.jets["btagWPs"].items():
            algo, wp = btag_wp
            event.btagged_jets_bdisc[btag_wp_name] = filter(
                lambda x, algo=algo, wp=wp: getattr(x, algo) > wp,
                event.good_jets
            )
            event.buntagged_jets_bdisc[btag_wp_name] = filter(
                lambda x, algo=algo, wp=wp: getattr(x, algo) <= wp,
                event.good_jets
            )
            if "jets" in self.conf.general["verbosity"] or "debug" in self.conf.general["verbosity"]:
                autolog("btagged jets", btag_wp_name, btag_wp, len(event.btagged_jets_bdisc[btag_wp_name]))
            setattr(event, "nB"+btag_wp_name, len(event.btagged_jets_bdisc[btag_wp_name]))

        #Find jets that pass/fail the specified default b-tagging algo/working point
        event.buntagged_jets_bdisc = event.buntagged_jets_bdisc[self.conf.jets["btagWP"]]
        event.btagged_jets_bdisc = event.btagged_jets_bdisc[self.conf.jets["btagWP"]]

        #Find how many of these tagged jets are actually true b jets
        if self.cfg_comp.isMC:
            event.n_tagwp_tagged_true_bjets = 0
            for j in event.btagged_jets_bdisc:
                if abs(j.mcFlavour) == 5:
                    event.n_tagwp_tagged_true_bjets += 1

        #Require at least 2 good resolved jets to continue analysis
        passes = True
        if event.is_sl and len(event.good_jets) < 3:
            if "debug" in self.conf.general["verbosity"]:
                autolog("fails because SL NJ<3")
            passes = False
        if event.is_dl:
            if len(event.good_jets) < 2:
                if "debug" in self.conf.general["verbosity"]:
                    autolog("fails because DL NJ<2")
                passes = False
        if event.is_fh:
            if len(event.good_jets) < 6:      
                passes = False        
            if len(event.good_jets) >=6:
                if event.good_jets[5].pt<self.conf.jets["pt_fh"]:
                    passes = False


        #Calculate jet corrections to MET
        corrMet_px = event.MET.px
        corrMet_py = event.MET.py
        sum_dEx = 0
        sum_dEy = 0
        if self.cfg_comp.isMC:
            for jet in event.good_jets:
                Prec = lvec(jet)
                Pgen = lvec(jet)
                Pgen.SetPtEtaPhiM(jet.mcPt, jet.mcEta, jet.mcPhi, jet.mcM)
                Erec = Prec.E()
                Egen = Pgen.E()
                dEx = (Erec-Egen) * Prec.Px()/Prec.P()
                dEy = (Erec-Egen) * Prec.Py()/Prec.P()
                sum_dEx += dEx
                sum_dEy += dEy
        corrMet_px += sum_dEx
        corrMet_py += sum_dEy
        event.MET_jetcorr = MET(px=corrMet_px, py=corrMet_py)
        event.passes_jet = passes
        
        #Do gen-jet analysis
        if self.cfg_comp.isMC:
            genjets = event.GenJet
            for jet in event.good_jets:
                pt1 = jet.mcPt
                eta1 = jet.mcEta
                phi1 = jet.mcPhi
                mass1 = jet.mcM
                lv1 = ROOT.TLorentzVector()
                lv1.SetPtEtaPhiM(pt1, eta1, phi1, mass1)
                for gj in genjets:
                    lv2 = lvec(gj)
                    if lv1.DeltaR(lv2) < 0.01:
                        jet.genjet = gj
                        genjets.remove(gj)
                        break

        return event
