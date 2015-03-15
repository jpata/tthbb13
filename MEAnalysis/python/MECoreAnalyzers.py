import ROOT
import itertools
from PhysicsTools.HeppyCore.framework.analyzer import Analyzer


#Load integrator
# ROOT.gSystem.Load("libFWCoreFWLite")
# ROOT.gROOT.ProcessLine('AutoLibraryLoader::enable();')
# ROOT.gSystem.Load("libFWCoreFWLite")
ROOT.gSystem.Load("libCintex")
ROOT.gROOT.ProcessLine('ROOT::Cintex::Cintex::Enable();')
ROOT.gSystem.Load("libTTHMEIntegratorStandalone")

from ROOT import MEM

CvectorPermutations = getattr(ROOT, "std::vector<MEM::Permutations::Permutations>")
CvectorPSVar = getattr(ROOT, "std::vector<MEM::PSVar::PSVar>")

def lvec(self):
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(self.pt, self.eta, self.phi, self.mass)
    return lv


class FilterAnalyzer(Analyzer):
    """
    A generic analyzer that may filter events.
    Counts events the number of processed and passing events.
    """
    def beginLoop(self, setup):
        super(FilterAnalyzer, self).beginLoop(setup)
        self.counters.addCounter("processing")
        self.counters["processing"].register("processed")
        self.counters["processing"].register("passes")

class LeptonAnalyzer(FilterAnalyzer):
    """
    Analyzes leptons and applies single-lepton and di-lepton selection.

    Relies on
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

                    leps = filter(
                        lambda x: (
                            x.pt > lepcuts["pt"]
                            and abs(x.eta) < lepcuts["eta"]
                            and abs(getattr(x, self.conf.leptons[l]["isotype"])) < lepcuts["iso"]
                        ), incoll
                    )

                    if b == "_veto":
                        good = getattr(event, "{0}_{1}".format(l, a))
                        leps = filter(lambda x: x not in good, leps)

                    if a == "tight":
                        leps = filter(
                            lambda x: x.tightId,
                            leps
                        )
                    elif a == "loose":
                        leps = filter(
                            lambda x: x.looseIdPOG,
                            leps
                        )
                    lep = sorted(leps, key=lambda x: x.pt, reverse=True)
                    sumleps += leps
                    lt = l + "_" + a + b
                    setattr(event, lt, leps)
                    setattr(event, "n_"+lt, len(leps))
                    self.counters["leptons"].inc(lt, len(leps))

                setattr(event, "lep_{0}".format(a+b), sumleps)
                setattr(event, "n_lep_{0}".format(a+b), len(sumleps))


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
            print "pathological SL && DL event: {0}".format(event)
            self.counters["processing"].inc("slanddl")
            passes = False

        if passes:
            self.counters["processing"].inc("passes")
        return passes



class JetAnalyzer(FilterAnalyzer):
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

        event.good_jets = sorted(
            filter(
                lambda x: (
                    x.pt > self.conf.jets["pt"]
                    and abs(x.eta) < self.conf.jets["eta"]
                ), event.Jet
            ),
            key=lambda x: x.pt, reverse=True
        )
        self.counters["jets"].inc("good", len(event.good_jets))

        event.btagged_jets = {}
        event.buntagged_jets = {}
        for (btag_wp_name, btag_wp) in self.conf.jets["btagWPs"].items():
            algo, wp = btag_wp
            event.btagged_jets[btag_wp_name] = filter(
                lambda x: getattr(x, algo) > wp,
                event.good_jets
            )
            event.buntagged_jets[btag_wp_name] = filter(
                lambda x: getattr(x, algo) <= wp,
                event.good_jets
            )
            self.counters["jets"].inc(btag_wp_name,
                len(event.btagged_jets[btag_wp_name])
            )
        event.buntagged_jets = event.buntagged_jets[self.conf.jets["btagWP"]]

        passes = len(event.good_jets) >= 4
        if passes:
            self.counters["processing"].inc("passes")

        return passes


class BTagLRAnalyzer(FilterAnalyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BTagLRAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.conf = cfg_ana._conf
        self.bTagAlgo = self.conf.jets["btagAlgo"]
        self.cplots = ROOT.TFile(self.conf.general["controlPlotsFile"])
        self.csv_pdfs = {
        }
        for x in ["b", "c", "l"]:
            for b in ["Bin0", "Bin1"]:
                self.csv_pdfs[(x, b)] = self.cplots.Get(
                    "csv_{0}_{1}__csv_rec".format(x, b)
                )

    def get_pdf_prob(self, flavour, _bin, csv):
        h = self.csv_pdfs[(flavour, _bin)]

        if csv < 0:
            csv = 0.0
        if csv > 1.0:
            csv = 1.0
        nb = h.FindBin(csv)
        #if csv = 1 -> goes into overflow and pdf = 0.0
        #as a solution, take the next-to-last bin
        if nb >= h.GetNbinsX():
            nb = nb - 1
        ret = h.GetBinContent(nb)
        return ret

    def beginLoop(self, setup):
        super(BTagLRAnalyzer, self).beginLoop(setup)

    def evaluate_jet_prob(self, csv, eta):
        _bin = "Bin1" if abs(eta)>1.0 else "Bin0"
        return (
            self.get_pdf_prob("b", _bin, csv),
            self.get_pdf_prob("c", _bin, csv),
            self.get_pdf_prob("l", _bin, csv)
        )

    def btag_likelihood(self, probs, nB, nC):

        perms = itertools.permutations(range(len(probs)))

        P = 0.0
        max_p = -1.0
        nperms = 0
        best_perm = None
        for perm in perms:
            p = 1.0

            for i in range(0, nB):
                p *= probs[perm[i]][0]
            for i in range(nB, nB + nC):
                p *= probs[perm[i]][1]
            for i in range(nB + nC, len(probs)):
                p *= probs[perm[i]][2]

            if p > max_p:
                best_perm = perm
                max_p = p

            P += p
            nperms += 1
        P = P / float(nperms)
        return P, best_perm
        #end permutation loop

    def process(self, event):
        self.counters["processing"].inc("processed")

        jet_probs = [
            self.evaluate_jet_prob(getattr(j, self.bTagAlgo), j.eta)
            for j in event.good_jets
        ]
        jet_csvs = [
            getattr(j, self.bTagAlgo)
            for j in event.good_jets
        ]

        best_4b_perm = 0
        best_2b_perm = 0
        event.btag_lr_4b, best_4b_perm = self.btag_likelihood(jet_probs, 4, 0)
        event.btag_lr_2b, best_2b_perm = self.btag_likelihood(jet_probs, 2, 0)

        # if event.btag_lr_2b == 0:
        #     for (csv, p) in zip(jet_csvs, jet_probs):
        #         print csv, p
        event.btag_LR_4b_2b = event.btag_lr_4b / (event.btag_lr_4b + event.btag_lr_2b)

        event.buntagged_jets_by_LR_4b_2b = [event.good_jets[i] for i in best_4b_perm[4:]]

        # print "N", len(event.good_jets), "uT", len(event.buntagged_jets), "uLR", len(event.buntagged_jets_by_LR_4b_2b)
        # print "lr={0:.6f}".format(event.btag_LR_4b_2b)
        # s = ""
        #
        # if len(event.good_jets)>6:
        #     for (nj, j) in enumerate(event.good_jets):
        #         s += "j {0:.4f} {1}".format(getattr(j, self.bTagAlgo), j.mcFlavour)
        #
        #         if nj in best_2b_perm[0:4]:
        #             s += " b"
        #
        #         if nj in best_2b_perm[4:]:
        #             s += " l"
        #         s += "\n"
        #     s = s[:-1]
        #     print s

        passes = True
        if passes:
            self.counters["processing"].inc("passes")

        return passes

class MECategoryAnalyzer(FilterAnalyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(MECategoryAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.cat_map = {"cat1": 1, "cat2": 2, "cat3": 3, "cat6":6}

    def beginLoop(self, setup):
        super(MECategoryAnalyzer, self).beginLoop(setup)

        for c in ["cat1", "cat2", "cat3", "cat6"]:
            self.counters["processing"].register(c)

    def process(self, event):
        self.counters["processing"].inc("processed")

        cat = ""
        if event.is_sl:
            if len(event.good_jets) == 5:
                cat = "cat1"
            elif len(event.good_jets) == 6:
                cat = "cat2"
            else:
                cat = "cat3"
        elif event.is_dl and len(event.good_jets)>=4:
            cat = "cat6"

        self.counters["processing"].inc(cat)
        event.cat = cat
        event.catn = self.cat_map[cat]

        passes = True
        if passes:
            self.counters["processing"].inc("passes")
        return passes

class WTagAnalyzer(FilterAnalyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(WTagAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(WTagAnalyzer, self).beginLoop(setup)



    def pair_mass(self, j1, j2):
        lv1, lv2 = [lvec(j) for j in [j1, j2]]
        tot = lv1 + lv2
        return tot.M()

    def find_best_pair(self, jets):
        ms = []
        done_pairs = set([])
        for i in range(len(jets)):
            for j in range(len(jets)):
                if (i,j) not in done_pairs and i!=j:
                    m = self.pair_mass(jets[i], jets[j])
                    ms += [(m, jets[i], jets[j])]
                    done_pairs.add((i,j))
                    done_pairs.add((j,i))
        ms = sorted(ms, key=lambda x: abs(x[0] - 80.0))
        return ms[0]

    def process(self, event):
        self.counters["processing"].inc("processed")

        event.Wmass = 0.0
        event.Wmass2 = 0.0
        if len(event.buntagged_jets)>=2:
            bpair = self.find_best_pair(event.buntagged_jets)
            event.Wmass = bpair[0]

        if len(event.buntagged_jets_by_LR_4b_2b)>=2:
            bpair = self.find_best_pair(event.buntagged_jets_by_LR_4b_2b)
            event.Wmass2 = bpair[0]

        passes = True
        if passes:
            self.counters["processing"].inc("passes")
        return passes

class GenRadiationModeAnalyzer(FilterAnalyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(GenRadiationModeAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(GenRadiationModeAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.counters["processing"].inc("processed")

        event.nMatchSimB = 0
        event.nMatchSimC = 0
        lv_bs = map(lvec, event.GenBQuarkFromTop)
        for jet in event.good_jets:
            lv_j = lvec(jet)

            if (lv_j.Pt() > 20 and abs(lv_j.Eta()) < 2.5):
                if any([lv_b.DeltaR(lv_j) < 0.5 for lv_b in lv_bs]):
                    continue
                absid = abs(jet.mcFlavour)
                if absid == 5:
                    event.nMatchSimB += 1
                if absid == 4:
                    event.nMatchSimC += 1

        passes = True
        if passes:
            self.counters["processing"].inc("passes")
        return passes

class MEAnalyzer(FilterAnalyzer):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(MEAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.integrator = MEM.Integrand(1+2+4)

        self.permutations = CvectorPermutations()
        self.permutations.push_back(MEM.Permutations.BTagged)
        self.permutations.push_back(MEM.Permutations.QUntagged)
        self.permutations.push_back(MEM.Permutations.QQbarSymmetry)
        self.permutations.push_back(MEM.Permutations.BBbarSymmetry)
        self.integrator.set_permutation_strategy(self.permutations)

        self.integrator.set_integrand(
            MEM.IntegrandType.Constant
            |MEM.IntegrandType.ScattAmpl
            |MEM.IntegrandType.DecayAmpl
            |MEM.IntegrandType.Jacobian
            |MEM.IntegrandType.PDF
            |MEM.IntegrandType.Transfer
        )
        self.integrator.set_ncalls(4000);
        self.integrator.set_sqrts(13000.);

        self.vars_to_integrate = CvectorPSVar()

    def add_obj(self, objtype, **kwargs):
        if kwargs.has_key("p4s"):
            pt, eta, phi, mass = kwargs.pop("p4s")
            v = ROOT.TLorentzVector()
            v.SetPtEtaPhiM(pt, eta, phi, mass);
        elif kwargs.has_key("p4c"):
            v = ROOT.TLorentzVector(*kwargs.pop("p4c"))
        obsdict = kwargs.pop("obsdict", {})

        o = MEM.Object(v, objtype)
        for k, v in obsdict.items():
            o.addObs(k, v)
        self.integrator.push_back_object(o)

    def beginLoop(self, setup):
        super(MEAnalyzer, self).beginLoop(setup)

    def process(self, event):
        self.counters["processing"].inc("processed")

        jets = event.good_jets
        leptons = event.good_leptons
        met = event.input.met_pt
        #print "MEMINTEG", len(jets), len(leptons)

        for jet in jets:
            self.add_obj(
                MEM.ObjectType.Jet,
                p4s=(jet.pt, jet.eta, jet.phi, jet.mass),
                obsdict={MEM.Observable.BTAG: jet.btagCSV}
            )
        for lep in leptons:
            self.add_obj(
                MEM.ObjectType.Lepton,
                p4s=(lep.pt, lep.eta, lep.phi, lep.mass),
                obsdict={MEM.Observable.CHARGE: lep.charge}
            )
        self.add_obj(
            MEM.ObjectType.MET,
            p4s=(met, 0, 0, met),
        )

        fstate = MEM.FinalState.TTH
        if len(leptons) == 2:
            fstate = MEM.FinalState.LL
        if len(leptons) == 1:
            fstate = MEM.FinalState.LH

        res = {}
        if event.cat in self.conf.general["calcMECategories"] and event.btag_LR_4b_2b > 0.8:
            for hypo in [MEM.Hypothesis.TTH, MEM.Hypothesis.TTBB]:
                r = self.integrator.run(
                    fstate,
                    hypo,
                    self.vars_to_integrate
                )
                res[hypo] = r
            print event.cat, event.btag_LR_4b_2b, res
            event.p_hypo_tth = res[MEM.Hypothesis.TTH]
            event.p_hypo_ttbb = res[MEM.Hypothesis.TTBB]

        self.integrator.next_event()
