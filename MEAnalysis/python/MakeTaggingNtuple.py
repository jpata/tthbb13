
########################################
# Imports
########################################

import os
import sys
import itertools

import ROOT

import TTH.TTHNtupleAnalyzer.AccessHelpers as AH

########################################
# Configuration
########################################

DEF_VAL_FLOAT = -9999.0

# Allow overrding input file from command line
if len(sys.argv)==2:
    infile_name = sys.argv[1]
else:
    infile_name = "output.root"

object_name = "hadtop_3j"
        

int_branches = []
float_branches = []


int_branches.append("is_signal")

for j in ["j1", "j2", "j3"]:
    float_branches.extend(["{0}_{1}".format(j, x) for x in ["pt", "eta", "phi", "mass", "btagCSV"]])

float_branches.extend(["j1j2_mass", "j1j3_mass", "j2j3_mass", "j1j2j3_mass", 
                       "frec", "min_btagCSV", "max_btagCSV",
                       "mean_btagCSV", "variance_btagCSV"])


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
    if not len([1 for j in jets if j.matchFlag==0])==2:
        return False

    # Look for 1 jets from b decay (from hadronic top)
    if not len([1 for j in jets if j.matchFlag==1 and j.matchBfromHadT==1])==1:
        return False

    return True


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
        v["is_signal"]  = is_signal_hadtop_3j(comb)
    else:
        v["is_signal"]  = -1

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

    mw_over_mt = 80.4 / 173.3    
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

    infile = ROOT.TFile(infile_name)
    intree = infile.Get('tree')

    n_entries = intree.GetEntries()

    # Define the name of the output file
    outfile_name = infile_name.replace(".root", object_name + ".root")
    outfile = ROOT.TFile( outfile_name, 'recreate')

    # Create dicitionaries to hold the information that will be
    # written as new branches
    variables      = {}
    variable_types = {}

    # Tree to store the output variables in
    outtree = ROOT.TTree("tree", "tree")

    AH.addScalarBranches(variables,
                         variable_types,
                         outtree,
                         int_branches,
                         datatype = 'int')

    AH.addScalarBranches(variables,
                         variable_types,
                         outtree,
                         float_branches,
                         datatype = 'float')


    ########################################
    # Event loop
    ########################################

    print "Will process {0} events".format(n_entries)

    for i_event in range(n_entries):

        # Progress
        if not i_event % 1000:
            print "{0:.1f}%".format( 100.*i_event /n_entries)

        intree.GetEntry( i_event )    

        # Only use odd events
        if not AH.getter(intree, "evt")  % 2 == 1:        
            continue

        # Only use semileptonic events
        if not AH.getter(intree, "is_sl"):
            continue

        # Use 6/4 events
        if not (AH.getter(intree, "numJets") >= 6 and AH.getter(intree, "nBCSVM") >= 4):
            continue

        jets = make_jets_hadtop_3j(intree)

        for comb in itertools.combinations(jets, 3):

            # Reset branches
            AH.resetBranches(variables, variable_types)

            # Calculate variables and put them into the tree
            for k,v in calc_vars_hadtop_3j(comb).iteritems():
                variables[k][0] = v
            outtree.Fill()    
        # End of loop over combinations
    # End of event loop

    # Save everything & exit cleanly
    outtree.AutoSave()
    outfile.Close()    





