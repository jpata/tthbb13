########################################
# Imports
########################################

import os
import sys
import pdb
import itertools
import random

import ROOT

import TTH.TTHNtupleAnalyzer.AccessHelpers as AH
from TTH.MEAnalysis.samples_base import getSitePrefix

########################################
# Configuration
########################################

DEF_VAL_FLOAT = -9999.0

ntpl = {"multiclass_6j": {"int_branches"   : [],
                          "float_branches" : ["l_pt", "l_eta", "l_phi", "l_pdgid",
                                              "met_pt", "met_phi"],
                          "vars"           : {},
                          "var_types"      : {}}
    }
           

ntpl["multiclass_6j"]["int_branches"].extend(["tt_class", "evt"])




for j in range(6):
    ntpl["multiclass_6j"]["float_branches"].extend(["j{0}_{1}".format(j, x) for x in ["pt", 
                                                                                      "eta", 
                                                                                      "phi", 
                                                                                      "mass", 
                                                                                      "btagCSV"]])


########################################
# Helper: make_jets
########################################

def make_jets(tree):

    # Loop over truth particles
    n_jets = tree.njets

    # Get jet branches
    jet_pt             = tree.jets_pt
    jet_eta            = tree.jets_eta
    jet_phi            = tree.jets_phi
    jet_mass           = tree.jets_mass
    jet_btagCSV        = tree.jets_btagCSV

    # Build jet objects (TLorentzVector + extra quantities)    
    jets = []
    for ij in range(n_jets):
        jet = AH.buildTlv(jet_pt[ij], jet_eta[ij], jet_phi[ij], jet_mass[ij])
        jet.btagCSV        = jet_btagCSV[ij]
        jet.index          = ij
        jets.append(jet)

    # Sort jets by pt
    jets.sort(key = lambda x:-x.Pt())

    return jets


########################################
# Helper: calc_vars
########################################

def calc_vars(tree):

    v = {}

    # Prepare objects
    jets = make_jets(tree)

    # Jet Variables
    for ij in range(6):
        v["j{0}_pt".format(ij)]      = jets[ij].Pt()
        v["j{0}_eta".format(ij)]     = jets[ij].Eta()
        v["j{0}_phi".format(ij)]     = jets[ij].Phi()
        v["j{0}_mass".format(ij)]    = jets[ij].M()
        v["j{0}_btagCSV".format(ij)] = max(jets[ij].btagCSV, 0)



    # Lepton Variables
    v["l_pt"]    = tree.leps_pt[0]
    v["l_eta"]   = tree.leps_eta[0]
    v["l_phi"]   = tree.leps_phi[0]
    v["l_pdgid"] = tree.leps_pdgId[0]

    # Missing Et
    v["met_pt"]   = tree.met_pt
    v["met_phi"]  = tree.met_phi

    # ttb
    if tree.ttCls == 51:
        tt_class = 1  
    # tt2b
    elif tree.ttCls == 52:
        tt_class = 2  
    # ttbb
    elif tree.ttCls == 53 or tree.ttCls == 54 or tree.ttCls == 55 or tree.ttCls==56:
        tt_class = 3  
    # ttcc 
    elif tree.ttCls == 41 or tree.ttCls == 42 or tree.ttCls == 43 or tree.ttCls == 44 or tree.ttCls == 45:
        tt_class = 4  
    # ttll
    elif tree.ttCls == 0 or tree.ttCls<0:
        tt_class = 0  
    # should not happen
    else:
        print "Error determining tt+jets subsample" 
        sys.exit()

    v["tt_class"] = tt_class

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

    if "FILE_NAMES" in os.environ.keys():
        for fi in os.environ["FILE_NAMES"].split(" "):
            print "adding", fi
            intree.AddFile(getSitePrefix(fi))
    else:
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

        # Use 6 jet events
        if not (AH.getter(intree, "numJets") >= 6):
            continue
            
        # Prepare multiclass - 6 jet ntuple
        if "multiclass_6j" in ntpl.keys():

            variables      = ntpl["multiclass_6j"]["vars"]
            variable_types = ntpl["multiclass_6j"]["var_types"]

            # Reset branches
            AH.resetBranches(variables, variable_types)


            # Calculate variables and put them into the tree
            for k,v in calc_vars(intree).iteritems():
                variables[k][0] = v

            variables["evt"][0] = AH.getter(intree, "evt")
                    
            ntpl["multiclass_6j"]["tree"].Fill()    

        # End of preparing multiclass - 6 jet ntuple

    # End of event loop

    # Save everything & exit cleanly
    for v in ntpl.values():
        v["tree"].AutoSave()
    
    outfile.Close()    





