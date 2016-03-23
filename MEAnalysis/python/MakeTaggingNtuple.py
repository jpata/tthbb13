########################################
# Imports
########################################

import os
import sys
import itertools
import random

import ROOT

import TTH.TTHNtupleAnalyzer.AccessHelpers as AH
from TTH.MEAnalysis.samples_base import getSitePrefix

########################################
# Configuration
########################################

# Take input files from command line

DEF_VAL_FLOAT = -9999.0
TOP_MASS = 172
MAX_PERM = 20
TOPEVENT_INCREASE_STAT = 50

ntpl = {"hadtop_3j": {"int_branches"      : [],
                         "float_branches" : [],
                         "vars"           : {},
                         "var_types"      : {}},

        "topevent": {"int_branches"   : [],
                     "float_branches" : [],
                     "vars"           : {},
                     "var_types"      : {}}
}
           
ntpl["hadtop_3j"]["int_branches"].extend(["is_signal",
                                          "w_matches",
                                          "b_matches",
                                          "evt"])

for j in ["j1", "j2", "j3"]:
    ntpl["hadtop_3j"]["float_branches"].extend(["{0}_{1}".format(j, x) for x in ["pt", 
                                                                                 "eta", 
                                                                                 "phi", 
                                                                                 "mass", 
                                                                                 "btagCSV"]])

ntpl["hadtop_3j"]["float_branches"].extend(["j1j2_mass", 
                                            "j1j3_mass", 
                                            "j2j3_mass", 
                                            "j1j2j3_mass", 
                                            "frec", 
                                            "min_btagCSV", 
                                            "max_btagCSV",
                                            "mean_btagCSV", 
                                            "variance_btagCSV"])

ntpl["topevent"]["int_branches"].extend(["evt", "good_perm_in_event", "good_perm_in_first_n"])

for ic in range(MAX_PERM):
    ntpl["topevent"]["float_branches"].extend(["c{0}_mass".format(ic), 
                                               "c{0}_frec".format(ic), 
                                               "c{0}_meanCSV".format(ic), 
                                               "c{0}_varCSV".format(ic)])



########################################
# Helper: is_signal_hadtop_3j
########################################

def is_signal_hadtop_3j(jets):
    """ Takes list of jets as input and returns bool. 

    True if each jet matches to a decay product from hadronic top,
    False otherwise.

    jets is a list of ROOT TLorentzVectors with extra
    properties. Necessary are matchFlag and matchBfromHadT.
    
    matchFlag:
      -1 not matched to anything
       0 W
       1 b from top
       2 b from Higgs

    matchBfromHadT:
      -1 not matched or not b or not from top
       0 b from leptonic top
       1 b from hadronic top
    """
    
    # We need exactly three jets
    if not len(jets)==3:
        return False

    # Look for 2 jets from W decay
    W_matches = len([1 for j in jets if j.matchFlag==0])

    # Look for 1 jets from b decay (from hadronic top)
    b_matches = len([1 for j in jets if j.matchFlag==1 and j.matchBfromHadT==1])

    #is_signal = (W_matches == 2) and (b_matches==1)

    if (W_matches==0) and (b_matches==0):
        is_signal = 0
    elif (W_matches==0) and (b_matches==1):
        is_signal = 1
    elif (W_matches==1) and (b_matches==0):
        is_signal = 2
    elif (W_matches==1) and (b_matches==1):
        is_signal = 3
    elif (W_matches==2) and (b_matches==0):
        is_signal = 4
    elif (W_matches==2) and (b_matches==1):
        is_signal = 5
    else:
        is_signal = -1



    return is_signal, W_matches, b_matches


########################################
# Helper: make_jets_hadtop_3j
########################################

def make_jets_hadtop_3j(tree, useTruth = True):

    # Loop over truth particles
    n_jets = tree.njets


    # Get jet branches
    jet_pt             = tree.jets_pt
    jet_eta            = tree.jets_eta
    jet_phi            = tree.jets_phi
    jet_mass           = tree.jets_mass
    jet_btagCSV        = tree.jets_btagCSV
    if useTruth:
        jet_matchFlag      = tree.jets_matchFlag
        jet_matchBfromHadT = tree.jets_matchBfromHadT

    # Build jet objects (TLorentzVector + extra quantities)    
    jets = []
    for ij in range(n_jets):
        jet = AH.buildTlv(jet_pt[ij], jet_eta[ij], jet_phi[ij], jet_mass[ij])
        jet.btagCSV        = jet_btagCSV[ij]
        if useTruth:
            jet.matchFlag      = jet_matchFlag[ij]
            jet.matchBfromHadT = jet_matchBfromHadT[ij]
        jet.index          = ij
        jets.append(jet)

    # Sort jets by pt
    jets.sort(key = lambda x:-x.Pt())

    return jets




########################################
# Helper: calc_vars_hadtop_3j
########################################

def calc_vars_hadtop_3j(comb, useTruth = True):

    v = {}

    if useTruth:
        ret = is_signal_hadtop_3j(comb)
        v["is_signal"]  = ret[0]
        v["w_matches"]  = ret[1]
        v["b_matches"]  = ret[2]
    else:
        v["is_signal"]  = -1
        v["w_matches"]  = -1
        v["b_matches"]  = -1

    # Leading pT jet
    v["j1_pt"]      = comb[0].Pt()
    v["j1_eta"]     = comb[0].Eta()
    v["j1_phi"]     = comb[0].Phi()
    v["j1_mass"]    = comb[0].M()
    v["j1_btagCSV"] = max(comb[0].btagCSV, 0)

    # Second pT jet
    v["j2_pt"]      = comb[1].Pt()
    v["j2_eta"]     = comb[1].Eta()
    v["j2_phi"]     = comb[1].Phi()
    v["j2_mass"]    = comb[1].M()
    v["j2_btagCSV"] = max(comb[1].btagCSV, 0)

    # Third pT jet
    v["j3_pt"]      = comb[2].Pt()
    v["j3_eta"]     = comb[2].Eta()
    v["j3_phi"]     = comb[2].Phi()
    v["j3_mass"]    = comb[2].M()
    v["j3_btagCSV"] = max(comb[2].btagCSV, 0)

    # Pairs and Triplet
    j1j2   = comb[0]+comb[1]
    j1j3   = comb[0]+comb[2]
    j2j3   = comb[1]+comb[2]
    j1j2j3 = comb[0]+comb[1]+comb[2]

    v["j1j2_mass"]   = j1j2.M()
    v["j1j3_mass"]   = j1j3.M()
    v["j2j3_mass"]   = j2j3.M()
    v["j1j2j3_mass"] = min(400, j1j2j3.M())

    mw_over_mt = 80.4 / TOP_MASS
    frec = min([ abs((x.M()/j1j2j3.M())/mw_over_mt - 1) for x in [j1j2, j1j3, j2j3]])
    v["frec"] = min(0.4, frec)

    # B-tagging
    csvs = [max(0,j.btagCSV) for j in comb]
    mean = sum(csvs) / len(csvs)
    v["min_btagCSV"]      = min(csvs)
    v["max_btagCSV"]      = max(csvs)
    v["mean_btagCSV"]     = mean
    v["variance_btagCSV"] = sum((mean - x) ** 2.0 for x in csvs) / len(csvs)

    return v

     
########################################
# Prepare input/output
########################################

if __name__ == "__main__":


    outfile = ROOT.TFile( sys.argv[1], "recreate")

    
    # Add trees for all the NTuples we want
    # Tree to store the output variables in
    for k,v in ntpl.iteritems():
        v["tree"] = ROOT.TTree(k,k)
        
        AH.addScalarBranches(v["vars"],
                             v["var_types"],
                             v["tree"],
                             v["int_branches"],                             
                             datatype = 'int')

        AH.addScalarBranches(v["vars"],
                             v["var_types"],
                             v["tree"],
                             v["float_branches"],                             
                             datatype = 'float')


    ########################################
    # Event loop
    ########################################

    intree = ROOT.TChain("tree")
    for fi in sys.argv[2:]:
        print "adding", fi
        intree.AddFile(getSitePrefix(fi))

    ## For local testing:
    #infile = ROOT.TFile(sys.argv[2])
    #intree = infile.Get('tree')

    n_entries = intree.GetEntries()

    print "Will process {0} events".format(n_entries)

    for i_event in range(n_entries):

        # Progress
        if not i_event % 1000:
            print "{0:.1f}%".format( 100.*i_event /n_entries)

        intree.GetEntry( i_event )    

        # Only use semileptonic events
        if not AH.getter(intree, "is_sl"):
            continue

        # Use 6/4 events
        if not (AH.getter(intree, "numJets") >= 6 and AH.getter(intree, "nBCSVM") >= 4):
            continue

        jets = make_jets_hadtop_3j(intree)
            
        # Calculate per triplet variables of all permutations
        all_combs = []
        for comb in itertools.combinations(jets, 3):
            all_combs.append(calc_vars_hadtop_3j(comb))

        # Prepare hadtop_3j ntuple
        if "hadtop_3j" in ntpl.keys():

            for comb in all_combs:

                variables      = ntpl["hadtop_3j"]["vars"]
                variable_types = ntpl["hadtop_3j"]["var_types"]
                
                # Reset branches
                AH.resetBranches(variables, variable_types)

                # Calculate variables and put them into the tree
                for k,v in comb.iteritems():
                    variables[k][0] = v

                variables["evt"][0] = AH.getter(intree, "evt")

                ntpl["hadtop_3j"]["tree"].Fill()    
            # End of loop over combinations
        # End of preparing hadtop_3j ntuple


        # Prepare topevent ntuple
        if "topevent" in ntpl.keys():

            variables      = ntpl["topevent"]["vars"]
            variable_types = ntpl["topevent"]["var_types"]

            sorted_combs = sorted(all_combs, key = lambda x:abs(x["j1j2j3_mass"] - TOP_MASS))
            sorted_combs = sorted_combs[:MAX_PERM]

            # Inflate statistics ( and make independent of ordering)
            for _ in range(TOPEVENT_INCREASE_STAT):

                random.shuffle(sorted_combs)

                # Reset branches
                AH.resetBranches(variables, variable_types)

                variables["evt"][0] = AH.getter(intree, "evt")
                variables["good_perm_in_event"][0] = any([c["is_signal"]==5 for c in sorted_combs])
                variables["good_perm_in_first_n"][0] = any([c["is_signal"]==5 for c in sorted_combs[:MAX_PERM]])

                for ic in range(MAX_PERM):                    
                    variables["c{0}_mass".format(ic)][0]     = sorted_combs[ic]["j1j2j3_mass"]
                    variables["c{0}_frec".format(ic)][0]     = sorted_combs[ic]["frec"]
                    variables["c{0}_meanCSV".format(ic)][0]  = sorted_combs[ic]["mean_btagCSV"]
                    variables["c{0}_varCSV".format(ic)][0]   = sorted_combs[ic]["variance_btagCSV"]

                ntpl["topevent"]["tree"].Fill()    
        # End of preparing topevent ntuple

    # End of event loop

    # Save everything & exit cleanly
    for v in ntpl.values():
        v["tree"].AutoSave()
    
    outfile.Close()    





