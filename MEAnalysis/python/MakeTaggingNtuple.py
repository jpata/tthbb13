########################################
# Imports
########################################

import os
import sys
import pdb
import itertools
import random

import ROOT

import TTH.MEAnalysis.AccessHelpers as AH
from TTH.MEAnalysis.samples_base import getSitePrefix


########################################
# Configuration
########################################

DEF_VAL_FLOAT = -9999.0

ntpl = {"multiclass_6j": {"int_branches"   : [],
                          "float_branches" : ["l_pt", "l_eta", "l_phi", "l_pdgid",
                                              "met_pt", "met_phi",
                                              "blr"
                                          ],
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

def make_jets(source, source_type = "tree"):

    if source_type == "tree":
        n_jets = source.njets

        # Get jet branches
        jet_pt             = source.jets_pt
        jet_eta            = source.jets_eta
        jet_phi            = source.jets_phi
        jet_mass           = source.jets_mass
        jet_btagCSV        = source.jets_btagCSV
    elif source_type == "event":
        n_jets = len(source.good_jets)

        # Get jet branches
        jet_pt             = [j.pt for j in source.good_jets]
        jet_eta            = [j.eta for j in source.good_jets]
        jet_phi            = [j.phi for j in source.good_jets]
        jet_mass           = [j.mass for j in source.good_jets]
        jet_btagCSV        = [j.btagCSV for j in source.good_jets]
        
    # Build jet objects (TLorentzVector + extra quantities)    
    jets = []
    for ij in range(n_jets):
        jet = AH.buildTlv(jet_pt[ij], jet_eta[ij], jet_phi[ij], jet_mass[ij])
        jet.btagCSV        = jet_btagCSV[ij]
        jet.index          = ij
        jets.append(jet)

    # Sort jets by pt
    #jets.sort(key = lambda x:-x.Pt())

    # Sort jets by CSV
    jets.sort(key = lambda x:-x.btagCSV)

    return jets


########################################
# Helper: calc_vars
########################################

def calc_vars(source, source_type="tree"):

    v = {}

    # Prepare objects
    jets = make_jets(source, source_type)

    # Jet Variables
    for ij in range(6):
        v["j{0}_pt".format(ij)]      = jets[ij].Pt()
        v["j{0}_eta".format(ij)]     = jets[ij].Eta()
        v["j{0}_phi".format(ij)]     = jets[ij].Phi()
        v["j{0}_mass".format(ij)]    = jets[ij].M()
        v["j{0}_btagCSV".format(ij)] = max(jets[ij].btagCSV, 0)

    # When reading from a file
    if source_type == "tree":
        # Lepton Variables
        v["l_pt"]    = source.leps_pt[0]
        v["l_eta"]   = source.leps_eta[0]
        v["l_phi"]   = source.leps_phi[0]
        v["l_pdgid"] = source.leps_pdgId[0]

        # Missing Et     
        v["met_pt"]   = source.met_pt
        v["met_phi"]  = source.met_phi
        
        # BLR
        v["blr"] = source.btag_LR_4b_2b_btagCSV

    # During a ttH/Heppy analyzer module
    elif source_type == "event":
        # Lepton Variables
        v["l_pt"]    = source.good_leptons[0].pt
        v["l_eta"]   = source.good_leptons[0].eta
        v["l_phi"]   = source.good_leptons[0].phi
        v["l_pdgid"] = source.good_leptons[0].pdgId

        # Missing Et     
        v["met_pt"]   = source.MET.pt
        v["met_phi"]  = source.MET.phi

        # BLR
        v["blr"] = source.btag_LR_4b_2b_btagCSV


    # ttb
    if source.ttCls == 51:
        tt_class = 0
    # tt2b
    elif source.ttCls == 52:
        tt_class = 1  
    # ttbb
    elif source.ttCls == 53 or source.ttCls == 54 or source.ttCls == 55 or source.ttCls==56:
        tt_class = 2  
    # ttcc 
    elif source.ttCls == 41 or source.ttCls == 42 or source.ttCls == 43 or source.ttCls == 44 or source.ttCls == 45:
        tt_class = 3  
    # ttll
    elif source.ttCls == 0 or source.ttCls<0:
        tt_class = 4  
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
            #intree.AddFile(fi)
        

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

        # Require at least two medium b-tags
        if not (AH.getter(intree, "nBCSVM") >= 2):
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





