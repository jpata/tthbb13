from TTH.MEAnalysis.VHbbTree import lvec

from TTH.MEAnalysis.Analyzer import FilterAnalyzer
class WTagAnalyzer(FilterAnalyzer):
    """
    Performs W-mass calculation on pairs of untagged jets.

    Jets are considered untagged according to the b-tagging permutation which
    gives the highest likelihood of the event being a 4b+Nlight event.
    """
    def __init__(self, cfg_ana, cfg_comp, looperName):
        self.conf = cfg_ana._conf
        super(WTagAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

    def beginLoop(self, setup):
        super(WTagAnalyzer, self).beginLoop(setup)

    def pair_mass(self, j1, j2):
        """
        Calculates the invariant mass of a two-particle system.
        """
        lv1, lv2 = [lvec(j) for j in [j1, j2]]
        tot = lv1 + lv2
        return tot.M()

    def find_best_pair(self, jets):
        """
        Finds the pair of jets whose invariant mass is closest to mW=80 GeV.
        Returns the sorted vector of [(mass, jet1, jet2)], best first.
        """
        ms = []

        #Keep track of index pairs already calculated
        done_pairs = set([])

        #Double loop over all jets
        for i in range(len(jets)):
            for j in range(len(jets)):

                #Make sure we haven't calculated this index pair yet
                if (i,j) not in done_pairs and i!=j:
                    m = self.pair_mass(jets[i], jets[j])
                    ms += [(m, jets[i], jets[j])]

                    #M(i,j) is symmetric, hence add both pairs
                    done_pairs.add((i,j))
                    done_pairs.add((j,i))
        ms = sorted(ms, key=lambda x: abs(x[0] - 80.0))
        return ms

    def process(self, event):
        self.counters["processing"].inc("processed")

        event.Wmass = 0.0

        #we keep a set of the Q quark candidate jets
        event.wquark_candidate_jets = set([])

        event.wquark_candidate_jet_pairs = []
        #Need at least 2 untagged jets to calculate W mass
        if len(event.buntagged_jets)>=2:
            bpair = self.find_best_pair(event.buntagged_jets)
            #Get the best mass
            event.Wmass = bpair[0][0]

            #All masses
            event.Wmasses = [bpair[i][0] for i in range(len(bpair))]

            #Add at most 2 best pairs two W quark candidates
            for i in range(min(len(bpair), 2)):
                event.wquark_candidate_jets.add(bpair[i][1])
                event.wquark_candidate_jets.add(bpair[i][2])
                event.wquark_candidate_jet_pairs += [(bpair[i][1], bpair[i][2])]

                if "reco" in self.conf.general["verbosity"]:
                    print("Wmass", event.Wmass,
                        event.good_jets.index(bpair[i][1]),
                        event.good_jets.index(bpair[i][2])
                    )
        #If we can't calculate W mass, untagged jets become the candidate
        else:
            for jet in event.buntagged_jets:
                event.wquark_candidate_jets.add(jet)
        if "reco" in self.conf.general["verbosity"]:
            for pair in event.wquark_candidate_jet_pairs:
                print "wqpair", pair[0].pt, pair[1].pt


        passes = True
        if passes:
            self.counters["processing"].inc("passes")
        return passes

