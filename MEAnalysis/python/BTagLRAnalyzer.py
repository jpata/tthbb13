import ROOT
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM
import itertools

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import lvec

import numpy as np
Cvectoruint = getattr(ROOT, "std::vector<unsigned int>")

class BTagLRAnalyzer(FilterAnalyzer):
    """
    Performs b-tag likelihood ratio calculations
    FIXME: doc
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BTagLRAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.bTagAlgo        = getattr(cfg_ana, "btagAlgo", self.conf.jets["btagAlgo"])
        #self.cplots_old = ROOT.TFile(self.conf.general["controlPlotsFileOld"])
        self.cplots = ROOT.TFile(self.conf.general["controlPlotsFile"])
        self.nJetsForPerm = self.conf.jets["NJetsForBTagLR"]

        self.csv_pdfs = {
        }
        
        #print "Need to Fix the BTagLRAnalyzer to return normalised PDFs"
        for x in ["b", "c", "l"]:
            for b in ["Bin0", "Bin1"]:
                self.csv_pdfs[(x, b)] = self.cplots.Get(
                    "{2}_{0}_{1}__rec".format(x, b, self.bTagAlgo)
                )
                #self.csv_pdfs[(x, b)].Scale(1.0 / self.csv_pdfs[(x, b)].Integral())
            self.csv_pdfs[(x, "pt_eta")] = self.cplots.Get(
                "{1}_{0}_pt_eta".format(x, self.bTagAlgo)
            )
         
            # consider also underflow and overflow bins (N.B. some jets have csv==1, i.e. they will fall into overflow)
            h3     = self.csv_pdfs[(x, "pt_eta")]
            nbinsX = h3.GetNbinsX()
            nbinsY = h3.GetNbinsY()
            nbinsZ = h3.GetNbinsZ()
            for i in range(0, nbinsX+2):
                for j in range(0, nbinsY+2):
                    int_ij = 0.
                    for k in range(0, nbinsZ+2):
                        int_ij += h3.GetBinContent(i,j,k)
                    for k in range(0, nbinsZ+2):
                        unnorm = h3.GetBinContent(i,j,k)
                        if int_ij>0.:
                            unnorm /= int_ij
                        self.csv_pdfs[(x, "pt_eta")].SetBinContent(i,j,k, unnorm)
        
        #print self.csv_pdfs

        self.conf.BTagLRAnalyzer = self
        self.jlh = MEM.JetLikelihood()

    def get_pdf_prob(self, flavour, pt, eta, csv, kind):

        _bin = "Bin1" if abs(eta)>1.0 else "Bin0"

        # if kind == "old":
        #     h = self.csv_pdfs_old[(flavour, _bin)]
        if kind == "new_eta_1bin":
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


    def btag_likelihood2(self, probs, nB):
        self.jlh.next_event()
        #print "njets", len(probs)
        for ijet in range(len(probs)):
            jp = ROOT.MEM.JetProbability()
            jp.setProbability(MEM.JetInterpretation.b, probs[ijet][0])
            jp.setProbability(MEM.JetInterpretation.c, probs[ijet][1])
            jp.setProbability(MEM.JetInterpretation.l, probs[ijet][2])
            self.jlh.push_back_object(jp)

        bperm = Cvectoruint()
        P = self.jlh.calcProbability(MEM.JetInterpretation.b, MEM.JetInterpretation.l, nB, bperm)
        best_perm = [bperm.at(i) for i in range(bperm.size())]

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
        return self.conf.general["passall"] or np.any([v.passes_btag for v in event.systResults.values()])

    def getJetProbs(self, event, taggers):
        jets_for_btag_lr = {}
        jet_probs        = {}
        
        for pdf in ["new_pt_eta_bin_3d"]:
            for csv in taggers:
                jets_for_btag_lr[ csv ] =  sorted(
                    event.good_jets, key=lambda x: getattr(x, csv, self.bTagAlgo), reverse=True
                )[0:6]
                jet_probs[ pdf+"-"+csv ] =  [ 
                    self.evaluate_jet_prob(j.pt, j.eta, getattr(j, csv, self.bTagAlgo), pdf)
                    for j in jets_for_btag_lr[ csv ]
                ]
        return jets_for_btag_lr, jet_probs

    def lratio(self, l1, l2):
        if l1+l2>0:
            return l1/(l1+l2)
        else:
            return 0.0

    def _process(self, event):

        #Take first 6 most b-tagged jets for btag LR
        jets_for_btag_lr, jet_probs = self.getJetProbs(
            event,
            #[self.bTagAlgo, "btagCSVRndge4t", "btagCSVInpge4t", "btagCSVRnd3t", "btagCSVInp3t"]
            [self.bTagAlgo]
        )

        # default
        # event.btag_lr_4b, best_4b_perm = self.btag_likelihood(jet_probs["new_pt_eta_bin_3d-"+self.bTagAlgo], 4, 0)
        # event.btag_lr_2b, best_2b_perm = self.btag_likelihood(jet_probs["new_pt_eta_bin_3d-"+self.bTagAlgo], 2, 0)

        #new, dedicated calculation
        event.btag_lr_4b, best_4b_perm = self.btag_likelihood2(jet_probs["new_pt_eta_bin_3d-"+self.bTagAlgo], 4)
        event.btag_lr_2b, best_2b_perm = self.btag_likelihood2(jet_probs["new_pt_eta_bin_3d-"+self.bTagAlgo], 2)

        #event.btag_LR_4b_2b = self.lratio(event.btag_lr_4b, event.btag_lr_2b)
        event.btag_LR_4b_2b = self.lratio(event.btag_lr_4b, event.btag_lr_2b)
    
        # use default btag method always
        event.buntagged_jets_by_LR_4b_2b = [jets_for_btag_lr[self.bTagAlgo][i] for i in best_4b_perm[4:]]
        event.btagged_jets_by_LR_4b_2b = [jets_for_btag_lr[self.bTagAlgo][i] for i in best_4b_perm[0:4]]

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

        btagged = sorted(event.selected_btagged_jets, key=lambda x: getattr(x, self.bTagAlgo) , reverse=True)

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

        event.passes_btag = len(event.selected_btagged_jets)>=0
        return event
