import ROOT
import itertools

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.VHbbTree import lvec

import numpy as np

class BTagLRAnalyzer(FilterAnalyzer):
    """
    Performs b-tag likelihood ratio calculations
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BTagLRAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.bTagAlgo = self.conf.jets["btagAlgo"]
        self.cplots_old = ROOT.TFile(self.conf.general["controlPlotsFileOld"])
        self.cplots = ROOT.TFile(self.conf.general["controlPlotsFile"])

        cplots_fmt = self.conf.general.get("controlPlotsFormat", "8tev")
        self.csv_pdfs_old = {
        }
        for x in ["b", "c", "l"]:
            for b in ["Bin0", "Bin1"]:
                self.csv_pdfs_old[(x, b)] = self.cplots_old.Get(
                    "csv_{0}_{1}__csv_rec".format(x, b)
                )

        self.csv_pdfs = {
        }
        
        print "Need to Fix the BTagLRAnalyzer to return normalised PDFs"
        for x in ["b", "c", "l"]:
            for b in ["Bin0", "Bin1"]:
                self.csv_pdfs[(x, b)] = self.cplots.Get(
                    "csv_{0}_{1}__csv_rec".format(x, b)
                )
                #self.csv_pdfs[(x, b)].Scale(1.0 / self.csv_pdfs[(x, b)].Integral())
            self.csv_pdfs[(x, "pt_eta")] = self.cplots.Get(
                "csv_{0}_pt_eta".format(x)
            )
            #self.csv_pdfs[(x, "pt_eta")].Scale(1.0 / self.csv_pdfs[(x, "pt_eta")].Integral())
            for i in range(1,  self.csv_pdfs[(x, "pt_eta")].GetNbinsX()+2 ):
                for j in range(1,  self.csv_pdfs[(x, "pt_eta")].GetNbinsY()+2 ):
                    h = self.csv_pdfs[(x, "pt_eta")].ProjectionZ("_pz", i,i, j,j)
                    #print h.GetEntries()
                    norm = h.Integral()
                    if norm == 0:
                        print "Bin ", i ,", " , j, " empty"
                        continue
                    for k in range(1,  self.csv_pdfs[(x, "pt_eta")].GetNbinsZ()+2 ):
                        tot  = self.csv_pdfs[(x, "pt_eta")].GetBinContent(i,j,k)
                        self.csv_pdfs[(x, "pt_eta")].SetBinContent(i,j,k, tot/norm )
                    h2 = self.csv_pdfs[(x, "pt_eta")].ProjectionZ("_pz", i,i, j,j)
                    print "After rescaling: ", h2.Integral()

        self.conf.BTagLRAnalyzer = self

    def get_pdf_prob(self, flavour, pt, eta, csv, kind):

        _bin = "Bin1" if abs(eta)>1.0 else "Bin0"

        if kind == "old":
            h = self.csv_pdfs_old[(flavour, _bin)]
        elif kind == "new_eta_1bin":
            h = self.csv_pdfs[(flavour, _bin)]
        elif kind == "new_pt_eta_bin_3d":
            h = self.csv_pdfs[(flavour, "pt_eta")]

        assert h != None, "flavour={0} kind={1}".format(flavour, kind)

        if csv < 0:
            csv = 0.0
        if csv > 1.0:
            csv = 1.0

        if kind == "old" or kind == "new_eta_1bin":
            nb = h.FindBin(csv)
            #if csv = 1 -> goes into overflow and pdf = 0.0
            #as a solution, take the next-to-last bin
            if nb >= h.GetNbinsX():
                nb = nb - 1
            ret = h.GetBinContent(nb)
        elif kind == "new_pt_eta_bin_3d":
            nb = h.FindBin(pt, abs(eta), csv)
            ret = h.GetBinContent(nb)
        return ret

    def beginLoop(self, setup):
        super(BTagLRAnalyzer, self).beginLoop(setup)

    def evaluate_jet_prob(self, pt, eta, csv, kind):
        return (
            self.get_pdf_prob("b", pt, eta, csv, kind),
            self.get_pdf_prob("c", pt, eta, csv, kind),
            self.get_pdf_prob("l", pt, eta, csv, kind)
        )

    def btag_likelihood(self, probs, nB, nC):

        perms = itertools.permutations(range(len(probs)))

        P = 0.0
        max_p = -1.0
        nperms = 0
        best_perm = None

        np = len(probs)
        for perm in perms:
            p = 1.0

            for i in range(0, nB):
                if i < np:
                    p *= probs[perm[i]][0]
            for i in range(nB, min(nB + nC, np)):
                if i < np:
                    p *= probs[perm[i]][1]
            for i in range(nB + nC, np):
                if i < np:
                    p *= probs[perm[i]][2]

            #print nperms, p, perm, max_p, best_perm
            if p > max_p:
                best_perm = perm
                max_p = p

            P += p
            nperms += 1
        P = P / float(nperms)
        assert nperms > 0
        return P, best_perm
        #end permutation loop

    def process(self, event):
        for (syst, event_syst) in event.systResults.items():
            if event_syst.passes_jet:
                res = self._process(event_syst)
                event.systResults[syst] = res
            else:
                event.systResults[syst].passes_btag = False
        #event.__dict__.update(evdict["nominal"].__dict__)
        #event.__dict__.update(event.systResults["nominal"].__dict__)
        return np.any([v.passes_btag for v in event.systResults.values()])

    def _process(self, event):
        #Take first 6 most b-tagged jets for btag LR
        jets_for_btag_lr = sorted(
            event.good_jets,
            key=lambda x: getattr(x, self.bTagAlgo),
            reverse=True,
        )[0:6]

        jet_probs = {
            kind: [
                self.evaluate_jet_prob(j.pt, j.eta, getattr(j, self.bTagAlgo), kind)
                for j in jets_for_btag_lr
            ]
            for kind in [
            "old", "new_eta_1bin",
            "new_pt_eta_bin_3d"
            ]
        }
        jet_probs["best_btag"] = [self.evaluate_jet_prob(j.pt, j.eta, getattr(j, self.bTagAlgo), "new_pt_eta_bin_3d") for j in jets_for_btag_lr[:4]]

        # for nj, j in enumerate(jets_for_btag_lr):
        #     print j.btagCSV, j.mcFlavour, jet_probs["old"][nj], jet_probs["new_eta_1bin"][nj], jet_probs["new_pt_eta_bin_3d"][nj]
        #
        jet_csvs = [
            getattr(j, self.bTagAlgo)
            for j in event.good_jets
        ]

        ph = None
        best_4b_perm = 0
        best_2b_perm = 0
        event.btag_lr_4b_old, ph = self.btag_likelihood(jet_probs["old"], 4, 0)
        event.btag_lr_2b_old, v = self.btag_likelihood(jet_probs["old"], 2, 0)

        event.btag_lr_4b, best_4b_perm = self.btag_likelihood(jet_probs["new_eta_1bin"], 4, 0)
        event.btag_lr_4b_1c, ph = self.btag_likelihood(jet_probs["new_eta_1bin"], 4, 1)
        event.btag_lr_2b_2c, ph = self.btag_likelihood(jet_probs["new_eta_1bin"], 2, 2)
        
        event.btag_lr_4b_max4, ph = self.btag_likelihood(jet_probs["best_btag"], 4, 0)
        event.btag_lr_2b_max4, ph = self.btag_likelihood(jet_probs["best_btag"], 2, 0)

        event.btag_lr_2b, best_2b_perm = self.btag_likelihood(jet_probs["new_eta_1bin"], 2, 0)
        event.btag_lr_2b_1c, best_2b_perm = self.btag_likelihood(jet_probs["new_eta_1bin"], 2, 1)

        event.btag_lr_4b_alt, best_4b_perm_alt = self.btag_likelihood(jet_probs["new_pt_eta_bin_3d"], 4, 0)
        event.btag_lr_2b_alt, best_2b_perm_alt = self.btag_likelihood(jet_probs["new_pt_eta_bin_3d"], 2, 0)

        def lratio(l1, l2):
            if l1+l2>0:
                return l1/(l1+l2)
            else:
                return 0.0

        event.btag_LR_4b_2b_old = lratio(event.btag_lr_4b_old, event.btag_lr_2b_old)
        event.btag_LR_4b_2b = lratio(event.btag_lr_4b, event.btag_lr_2b)
        event.btag_LR_4b_2b_alt = lratio(event.btag_lr_4b_alt, event.btag_lr_2b_alt)
        event.btag_LR_4b_2b_max4 = lratio(event.btag_lr_4b_max4, event.btag_lr_2b_max4)

        event.buntagged_jets_by_LR_4b_2b = [jets_for_btag_lr[i] for i in best_4b_perm[4:]]
        event.btagged_jets_by_LR_4b_2b = [jets_for_btag_lr[i] for i in best_4b_perm[0:4]]

        for i in range(len(event.good_jets)):
            event.good_jets[i].btagFlag = 0.0

        #Jets are untagged according to the b-tagging likelihood ratio permutation
        if self.conf.jets["untaggedSelection"] == "btagLR":
            event.buntagged_jets = event.buntagged_jets_by_LR_4b_2b
            event.selected_btagged_jets = event.btagged_jets_by_LR_4b_2b
        #Jets are untagged according to b-discriminatr
        elif self.conf.jets["untaggedSelection"] == "btagCSV":
            event.buntagged_jets = event.buntagged_jets_bdisc
            event.selected_btagged_jets = event.btagged_jets_bdisc

        btagged = sorted(event.selected_btagged_jets, key=lambda x: x.btagCSV, reverse=True)

        #Take first 4 most b-tagged jets, these are used for the top and higgs candidates
        event.selected_btagged_jets_high = btagged[0:4]

        #any leftover b-tagged jets could be used for the W reconstruction
        event.selected_btagged_jets_low = btagged[4:]

        #Set these jets to be used as b-quarks in the MEM
        #We don't want to use more than 4 b-quarks in the hypothesis
        for jet in event.selected_btagged_jets_high:
            #idx = event.good_jets.index(jet)
            #event.good_jets[idx].btagFlag = 1.0
            jet.btagFlag = 1.0

        event.passes_btag = len(event.selected_btagged_jets)>=1
        return event
