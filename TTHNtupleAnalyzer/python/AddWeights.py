#!/usr/bin/env python
"""
Add an additional branch to an existing flat Ntuple.

Use to add a weight-branch to the Ntuples for tagging studies. 
Also add a true pt branch (either filled by hadtop_pt or parton_pt).
"""

########################################
# Imports
########################################

import pickle

import ROOT

import TTH.TTHNtupleAnalyzer.AccessHelpers as AH


########################################
# Configuration
########################################

basepath = '/scratch/gregor/'

#input_name = "ntop_v14_zprime_m2000_1p_13tev-tagging"     
input_name = "ntop_v14_qcd_800_1000_pythia8_13tev-tagging"     
input_tree_name = "tree"

input_pickle_file_name = "/shome/gregor/TTH-73X/CMSSW/src/TTH/Plotting/python/gregor/flat_pt_weights.pickle"


########################################
# Setup I/O
########################################

input_root_file_name = basepath + input_name + ".root"
output_root_file_name = basepath + input_name + "-weighted.root"

input_root_file = ROOT.TFile(input_root_file_name)
input_tree = input_root_file.Get(input_tree_name)

n_entries = input_tree.GetEntries()

output_root_file = ROOT.TFile(output_root_file_name, 'recreate')
output_tree = input_tree.CloneTree(0)


########################################
# Setup Variables
########################################

# Create dicitionaries to hold the information that will be
# written as new branches
variables      = {}
variable_types = {}

# Setup the output branches for the true object
AH.addScalarBranches(variables,
                     variable_types,
                     output_tree,
                     ["weight","pt"],
                     datatype = 'float')


########################################
# Get the weight function
########################################

# The pickle file contains a dictionary that gives us:
#   - a function f (fit of the pT spectrum)
#   - correct variable
# The weight is actually 1/(f)
# Example:
# { "ntop_v8_zprime_m2000_1p_13tev-tagging" : [ROOT.TF1(..), "hadtop"], ...}

pickle_file = open(input_pickle_file_name)
functions_and_parameter = pickle.load(pickle_file)

fun = functions_and_parameter[input_name][0]
param_name = functions_and_parameter[input_name][1]

print "Read from file: "
print fun, param_name


########################################
# Event loop
########################################

print "Processing {0} events".format(n_entries)

for i_event in range(n_entries):

    # Progress
    if not i_event % 1000:
        print "{0:.1f}%".format( 100.*i_event /n_entries)

    # Reset branches
    AH.resetBranches(variables, variable_types)

    input_tree.GetEntry( i_event )    

    # Calculate the weight
    pt = AH.getter(input_tree, param_name)
    value = fun(pt)
    if value > 0:
        weight = 1/(value)
    else:
        weight = 0
        
    variables["weight"][0] = weight
    variables["pt"][0]     = pt

    output_tree.Fill()
# End of event loop
    

output_tree.AutoSave()
output_root_file.Close()
input_root_file.Close()
