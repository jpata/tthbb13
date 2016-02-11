
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

float_branches.extend(["j1j2_mass", "j1j3_mass", "j2j3_mass", "j1j2j3_mass", "frec", "min_btagCSV", "max_btagCSV"])



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
# Prepare input/output
########################################

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

    # Only use semileptonic events
    if not AH.getter(intree, "is_sl"):
        continue

    # Only use odd semileptonic events
    if not AH.getter(intree, "evt")  % 2 == 1:        
        continue

    # Loop over truth particles
    n_jets = AH.getter(intree, "njets")
            
    # Get jet branches
    jet_pt             = AH.getter(intree, "jets_pt")
    jet_eta            = AH.getter(intree, "jets_eta")
    jet_phi            = AH.getter(intree, "jets_phi")
    jet_mass           = AH.getter(intree, "jets_mass")
    jet_btagCSV        = AH.getter(intree, "jets_btagCSV")
    jet_matchFlag      = AH.getter(intree, "jets_matchFlag")
    jet_matchBfromHadT = AH.getter(intree, "jets_matchBfromHadT")

    # Build jet objects (TLorentzVector + some extra quantities)    
    jets = []
    for ij in range(n_jets):
        jet = AH.buildTlv(jet_pt[ij], jet_eta[ij], jet_phi[ij], jet_mass[ij])
        jet.btagCSV        = jet_btagCSV[ij]
        jet.matchFlag      = jet_matchFlag[ij]
        jet.matchBfromHadT = jet_matchBfromHadT[ij]
        jets.append(jet)
    
    # Sort jets by pt
    jets.sort(key = lambda x:-x.Pt())
    
    for comb in itertools.combinations(jets, 3):
        
        # Reset branches
        AH.resetBranches(variables, variable_types)
        
        variables["is_signal"][0]  = is_signal_hadtop_3j(comb)
    
        variables["j1_pt"][0]      = comb[0].Pt()
        variables["j1_eta"][0]     = comb[0].Eta()
        variables["j1_phi"][0]     = comb[0].Phi()
        variables["j1_mass"][0]    = comb[0].M()
        variables["j1_btagCSV"][0] = max(comb[0].btagCSV, 0)

        variables["j2_pt"][0]      = comb[1].Pt()
        variables["j2_eta"][0]     = comb[1].Eta()
        variables["j2_phi"][0]     = comb[1].Phi()
        variables["j2_mass"][0]    = comb[1].M()
        variables["j2_btagCSV"][0] = max(comb[1].btagCSV, 0)

        variables["j3_pt"][0]      = comb[2].Pt()
        variables["j3_eta"][0]     = comb[2].Eta()
        variables["j3_phi"][0]     = comb[2].Phi()
        variables["j3_mass"][0]    = comb[2].M()
        variables["j3_btagCSV"][0] = max(comb[2].btagCSV, 0)

        j1j2   = comb[0]+comb[1]
        j1j3   = comb[0]+comb[2]
        j2j3   = comb[1]+comb[2]
        j1j2j3 = comb[0]+comb[1]+comb[2]

        variables["j1j2_mass"][0]   = j1j2.M()
        variables["j1j3_mass"][0]   = j1j3.M()
        variables["j2j3_mass"][0]   = j2j3.M()
        variables["j1j2j3_mass"][0] = j1j2j3.M()
        
        mw_over_mt = 80.4 / 173.3    
        frec = min([ abs((x.M()/j1j2j3.M())/mw_over_mt - 1) for x in [j1j2, j1j3, j2j3]])

        variables["frec"][0] = frec
        
        variables["min_btagCSV"][0] = max(min([j.btagCSV for j in comb]),0)
        variables["max_btagCSV"][0] = max(max([j.btagCSV for j in comb]),0)

        
        

        # Fill the tree   
        outtree.Fill()    

# Save everything & exit cleanly
outtree.AutoSave()
outfile.Close()    
    




