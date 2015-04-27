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
from TTH.Plotting.gregor.TopSamples import files 
from TTH.Plotting.gregor.HiggsSamples import files 


########################################
# Configuration
########################################

basepath = '/scratch/gregor/'

#to_process  = ["zprime_m1000"]
to_process  = files.keys()

for k in to_process:
    print "doing", k

    input_name = files[k]
    input_tree_name = "tree"

    input_pickle_file_name = "/shome/gregor/TTH-73X/CMSSW/src/TTH/Plotting/python/gregor/flat_pt_weights_higgs.pickle"


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
                         ["weight","pt", "eta"],
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

    try:
        pickle_file = open(input_pickle_file_name)

        functions_and_parameter_pt  = pickle.load(pickle_file)
        #functions_and_parameter_eta = pickle.load(pickle_file)

        pt_fun = functions_and_parameter_pt[input_name][0]
        pt_param_name = functions_and_parameter_pt[input_name][1]

        #eta_fun = functions_and_parameter_eta[input_name][0]
        #eta_param_name = functions_and_parameter_eta[input_name][1]

    except KeyError:
        print "WARNING: No weight function found for", input_name
        print "Using 1.0 as weight"
        print "This only makes sense for tth and ttj for Higgs tagging"
        
        if ("tth" in k or "rad_hh4b" in k):            
            pt_param_name = "higgs_pt"
            eta_param_name = "higgs_eta"
        elif ("ttj" in k or "qcd" in k):            
            pt_param_name = "parton_pt"
            eta_param_name = "parton_eta"

        pt_fun = lambda x:1.
        eta_fun = lambda x:1.


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
        pt = AH.getter(input_tree, pt_param_name)
        #eta = AH.getter(input_tree, eta_param_name)
        value = pt_fun(pt) #* eta_fun(eta)
        if value > 0:
            weight = 1/(value)
        else:
            weight = 0

        variables["weight"][0] = weight
        #variables["eta"][0]    = eta
        variables["pt"][0]     = pt

        output_tree.Fill()
    # End of event loop


    output_tree.AutoSave()
    output_root_file.Close()
    input_root_file.Close()
