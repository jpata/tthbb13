import ROOT
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")
from ROOT import MEM
import itertools
import math

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
from TTH.MEAnalysis.vhbb_utils import lvec, autolog

import numpy as np
Cvectoruint = getattr(ROOT, "std::vector<unsigned int>")

def logit(x):
    return math.log(x/(1.0 - x)) if x > 0 else -10

class BTagLRAnalyzer(FilterAnalyzer):
    """
    Performs b-tag likelihood ratio calculations
    FIXME: doc
    """

    def getPdfs(self, cplots):
        """
        Returns a dictionary with the b-tagging PDF-s
        """
        csv_pdfs = {}

        for x in ["b", "c", "l"]:
            for b in ["Bin0", "Bin1"]:
                csv_pdfs[(x, b)] = cplots.Get(
                    "{2}_{0}_{1}__rec".format(x, b, self.bTagAlgo)
                )
            csv_pdfs[(x, "pt_eta")] = cplots.Get(
                "{1}_{0}_pt_eta".format(x, self.bTagAlgo)
            )
        return csv_pdfs

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BTagLRAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.bTagAlgo        = self.conf.jets["btagAlgo"]
        #self.cplots_old = ROOT.TFile(self.conf.general["controlPlotsFileOld"])
        self.cplots = ROOT.TFile(self.conf.general["controlPlotsFile"])
        #self.cplots_new = ROOT.TFile(self.conf.general["controlPlotsFileNew"])

        self.csv_pdfs = self.getPdfs(self.cplots)
        #self.csv_pdfs_new = self.getPdfs(self.cplots_new)

        self.conf.BTagLRAnalyzer = self
        self.jlh = MEM.JetLikelihood()

    def get_pdf_prob(self, csv_pdfs, flavour, pt, eta, taggerval, kind):

        if kind == "new_eta_1bin":
            _bin = "Bin1" if abs(eta)>1.0 else "Bin0"
            h = csv_pdfs[(flavour, _bin)]
        elif kind == "new_pt_eta_bin_3d":
            h = csv_pdfs[(flavour, "pt_eta")]

        assert h != None, "flavour={0} kind={1}".format(flavour, kind)

        if kind == "new_eta_1bin":
            nb = h.FindBin(taggerval)
            if nb >= h.GetNbinsX():
                nb = h.GetNbinsX()
            elif nb < 1:
                nb = 1
            ret = h.GetBinContent(nb)
        elif kind == "new_pt_eta_bin_3d":
            nb = h.FindBin(pt, abs(eta), taggerval)
            ret = h.GetBinContent(nb)
        return ret

    def beginLoop(self, setup):
        super(BTagLRAnalyzer, self).beginLoop(setup)

    def evaluate_jet_prob(self, pdfs, pt, eta, taggerval, kind):
        return (
            self.get_pdf_prob(pdfs, "b", pt, eta, taggerval, kind),
            self.get_pdf_prob(pdfs, "c", pt, eta, taggerval, kind),
            self.get_pdf_prob(pdfs, "l", pt, eta, taggerval, kind)
        )

    def btag_likelihood2(self, probs, nB):
        self.jlh.next_event()
        for ijet in range(len(probs)):
            jp = ROOT.MEM.JetProbability()
            jp.setProbability(MEM.JetInterpretation.b, probs[ijet][0])
            jp.setProbability(MEM.JetInterpretation.c, probs[ijet][1])
            jp.setProbability(MEM.JetInterpretation.l, probs[ijet][2])
            self.jlh.push_back_object(jp)
            #print "probas", ijet, probs[ijet]

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
        return self.conf.general["passall"] or np.any([v.passes_btag for v in event.systResults.values()])

    def getJetProbs(self, pdfs, event, taggers):
        jets_for_btag_lr = {}
        jet_probs        = {}
        
        for pdf in ["new_pt_eta_bin_3d"]:
            for tagger in taggers:
                #Use only the first N jets by blr for likelihood ratio calculation 
                jets_for_btag_lr[tagger] =  sorted(
                    event.good_jets, key=lambda x, tagger=tagger: getattr(x, tagger), reverse=True
                )[0:self.conf.jets["NJetsForBTagLR"]]
                if tagger == "btagBDT":
                    tagtransform = lambda x: math.log((1.0 + x)/(1.0 - x)) if x > -1 else -10
                else:
                    tagtransform = lambda x: x
                jet_probs[pdf+"-"+tagger] =  [ 
                    self.evaluate_jet_prob(pdfs, j.pt, j.eta, tagtransform(getattr(j, tagger)), pdf)
                    for j in jets_for_btag_lr[tagger]
                ]
        return jets_for_btag_lr, jet_probs

    def lratio(self, l1, l2):
        if l1+l2>0:
            return l1/(l1+l2)
        else:
            return 0.0

    def _process(self, event):

        #btag algos for which to calculate btag LR
        btagalgos = [self.bTagAlgo]
        if self.conf.bran["enabled"]:
            btagalgos += ["btagCSVRndge4t", "btagCSVInpge4t", "btagCSVRnd3t", "btagCSVInp3t"]
        jets_for_btag_lr, jet_probs = self.getJetProbs(self.csv_pdfs, event, btagalgos )

        btag_likelihood_results = {}
        btag_likelihood_ratio_results = {}
        for btagalgo in btagalgos:
            btag_lr_4b, best_4b_perm = self.btag_likelihood2(jet_probs["new_pt_eta_bin_3d-" + btagalgo], 4)
            btag_lr_2b, best_2b_perm = self.btag_likelihood2(jet_probs["new_pt_eta_bin_3d-" + btagalgo], 2)
            btag_likelihood_results[btagalgo] = (btag_lr_4b, btag_lr_2b, best_4b_perm, best_2b_perm)
            btag_likelihood_ratio_results[btagalgo] = self.lratio(btag_lr_4b, btag_lr_2b)
        
        #default btagger used
        event.btag_lr_4b = btag_likelihood_results[self.bTagAlgo][0]
        event.btag_lr_2b = btag_likelihood_results[self.bTagAlgo][1]
        event.btag_LR_4b_2b = btag_likelihood_ratio_results[self.bTagAlgo]
        best_4b_perm = btag_likelihood_results[self.bTagAlgo][2]

        # use default btag method always
        event.buntagged_jets_by_LR_4b_2b = [jets_for_btag_lr[self.bTagAlgo][i] for i in best_4b_perm[4:]]
        event.btagged_jets_by_LR_4b_2b = [jets_for_btag_lr[self.bTagAlgo][i] for i in best_4b_perm[0:4]]

        for i in range(len(event.good_jets)):
            event.good_jets[i].btagFlag = 0.0

        #Jets are untagged according to the b-tagging likelihood ratio permutation
        if self.conf.jets["untaggedSelection"] == "btagLR":
            if "debug" in self.conf.general["verbosity"]:
                autolog("using btagLR for btag/untag jet selection")
            event.buntagged_jets = event.buntagged_jets_by_LR_4b_2b
            event.selected_btagged_jets = event.btagged_jets_by_LR_4b_2b
        #Jets are untagged according to b-discriminatr
        elif self.conf.jets["untaggedSelection"] == "btagCSV":
            if "debug" in self.conf.general["verbosity"]:
                autolog("using btagCSV for btag/untag jet selection")
            event.buntagged_jets = event.buntagged_jets_bdisc
            event.selected_btagged_jets = event.btagged_jets_bdisc
        if "debug" in self.conf.general["verbosity"]:
            autolog("N(untagged)={0} N(tagged)={1}".format(
                len(event.buntagged_jets),
                len(event.selected_btagged_jets)
            ))

        btagged = sorted(event.selected_btagged_jets, key=lambda x, self=self: getattr(x, self.bTagAlgo) , reverse=True)

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
        if "debug" in self.conf.general["verbosity"]:
            autolog("BTag selection pass={0}, len(btagged_jets)={1} using the method={2}".format(
                event.passes_btag,
                len(event.selected_btagged_jets),
                self.conf.jets["untaggedSelection"]
            ))

        #do category-specific blr cuts
        cat = ""
        if event.is_sl:
            cat += "sl_"

            if len(event.good_jets) == 4:
                cat += "j4_"
            elif len(event.good_jets) == 5:
                cat += "j5_"
            elif len(event.good_jets) >= 6:
                cat += "jge6_"

            if event.nBCSVM == 2:
                cat += "t2"
            elif event.nBCSVM == 3:
                cat += "t3"
            elif event.nBCSVM >= 4:
                cat += "tge4"
            else:
                cat = "unknown"
        elif event.is_dl:
            cat += "dl_"
            if len(event.good_jets)==3 and event.nBCSVM==2:
                cat += "j3_t2"
            elif len(event.good_jets)==3 and event.nBCSVM==3:
                cat += "j3_t3"
            elif len(event.good_jets)>=4 and event.nBCSVM==3:
                cat += "jge4_t3"
            elif len(event.good_jets)>=4 and event.nBCSVM==2:
                cat += "jge4_t2"
            elif len(event.good_jets)>=4 and event.nBCSVM>=4:
                cat += "jge4_tge4"
            else:
                cat = "unknown"
        else:
            cat = "unknown"

        event.category_string = cat
        blr_cut = self.conf.mem["blr_cuts"].get(cat, -20)
        if cat != "unknown":
            event.pass_category_blr = logit(event.btag_LR_4b_2b) > blr_cut 
        else:
            event.pass_category_blr = False
        if "debug" in self.conf.general["verbosity"]:
            autolog("SL/DL category: {0}, pass blr cut {1}: {2}".format(
                event.category_string, blr_cut, event.pass_category_blr)
            )
        return event
