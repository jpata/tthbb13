""" MakeTaggingNtuple: 
  - Take the output of the TTHNtupleAnalyzer
  - loop over the events and create a new output tree so that:
     - one event in the new tree corresponds to one true top/higgs/parton
     - and all the associated jets and taggers

  Goal: 
  - creation of efficiency curves
  - ROC curves
  - tagger correlation studies
"""

########################################
# Imports
########################################

import os
import sys
import glob
import socket

import ROOT

# for working on tier 3
if socket.gethostname() == "t3ui12":
    import TTH.TTHNtupleAnalyzer.AccessHelpers as AH
# on the Grid
else:
    import AccessHelpers as AH


########################################
# Configuration
########################################

DEF_VAL_FLOAT = -9999.0

# Allow overrding input file from command line
if len(sys.argv)==2:
    infile_name = sys.argv[1]
else:
    infile_name = "output.root"

# Determine particle species
# Tier3
if socket.gethostname() == "t3ui12":
    particle_name = "parton"
# Grid
else:
    import PSet
    initial_miniAOD_filename = list(PSet.process.source.fileNames)[0]
    if "ZPrimeToTTJets" in initial_miniAOD_filename:
        particle_name = "hadtop"
    elif "TTbarH_HToBB_M" in initial_miniAOD_filename:
        particle_name = "higgs"
    else:
        particle_name = "parton"


    print "Initial MiniAOD filename:", initial_miniAOD_filename
    print "Determined particle_name:", particle_name
        

particle_branches = ["pt", "eta", "phi", "mass"]

# "Normal" branches for most fatjet collections
fj_branches = ["pt", "mass", "tau1", "tau2", "tau3", "btag"]
# Extended fj branches, including shower deconstruction chi
# (to expensive to calc for everything)
fj_branches_chi = fj_branches + ["chi"]

htt_branches = ["pt", "mass", "fW", "Rmin", "RminExpected", "prunedMass"]
cmstt_branches = ["pt", "mass", "minMass", "wMass", "topMass"]

objects = {
    "ca08"           : fj_branches_chi,
    "ca08filtered"   : fj_branches,
    "ca08pruned"     : fj_branches,
    "ca08trimmed"    : fj_branches,
    "ca08softdrop"   : fj_branches,
    
    "ca15"           : fj_branches_chi,
    "ca15filtered"   : fj_branches,
    "ca15pruned"     : fj_branches,
    "ca15trimmed"    : fj_branches,
    "ca15softdrop"   : fj_branches,
    
    "ca08cmstt"      : cmstt_branches,
    "ca15cmstt"      : cmstt_branches,

    "looseMultiRHTT" : htt_branches,
}

# Matching DeltaR for the varipus object types
object_drs = {                      
    "ca08"           : 0.6,
    "ca08filtered"   : 0.6,
    "ca08pruned"     : 0.6,
    "ca08trimmed"    : 0.6,
    "ca08softdrop"   : 0.6,
    
    "ca15"           : 1.2,
    "ca15filtered"   : 1.2,
    "ca15pruned"     : 1.2,
    "ca15trimmed"    : 1.2,
    "ca15softdrop"   : 1.2,
    
    "ca08cmstt"      : 0.6,
    "ca15cmstt"      : 1.2,
    
    "looseMultiRHTT" : 1.2
}


########################################
# Prepare input/output
########################################

infile = ROOT.TFile(infile_name)
intree = infile.Get('tthNtupleAnalyzer/events')

branches_in_input = [b.GetName() for b in intree.GetListOfBranches()]

n_entries = intree.GetEntries()

# Define the name of the output file
outfile_name = infile_name.replace(".root","-tagging.root")

outfile = ROOT.TFile( outfile_name, 'recreate')

# Create dicitionaries to hold the information that will be
# written as new branches
variables      = {}
variable_types = {}

# Tree to store the output variables in
outtree = ROOT.TTree("tree", "tree")

# Setup the output branches for the true object
AH.addScalarBranches(variables,
                     variable_types,
                     outtree,
                     ["{0}_{1}".format(particle_name, branch_name) for branch_name in particle_branches],
                     datatype = 'float')

# Setup the output branches for tagging variables
for object_name, branch_names in objects.iteritems():    
    for branch_name in branch_names:

        full_branch_in  = "jet_{0}__{1}".format(object_name, branch_name)
        full_branch_out =  "{0}_{1}".format(object_name, branch_name)

        if full_branch_in in branches_in_input:
            AH.addScalarBranches( variables,
                                  variable_types,
                                  outtree,
                                  [full_branch_out],
                                  datatype = 'float')
        else:
            print "Warning: Branch {0} not available in input file. Removing full object {1}".format(full_branch_in, object_name)
            objects.pop(object_name, 0)
# End of loop over objects and branches


########################################
# Event loop
########################################

print "Will process {0} events".format(n_entries)

for i_event in range(n_entries):

    # Progress
    if not i_event % 1000:
        print "{0:.1f}%".format( 100.*i_event /n_entries)

    intree.GetEntry( i_event )    

    # Loop over truth particles
    n_particles = len(AH.getter( intree, "gen_{0}__pt".format(particle_name)))

    for i_particle in range(n_particles):

        # Reset branches
        AH.resetBranches(variables, variable_types)

        # Fill truth particle branches
        for branch_name in particle_branches:
            full_branch_in  = "gen_{0}__{1}".format(particle_name, branch_name)
            full_branch_out = "{0}_{1}".format(particle_name, branch_name)
            variables[full_branch_out][0] = AH.getter(intree, full_branch_in)[i_particle]


        # Fill fatjets and taggers
        for object_name, branch_names in objects.iteritems():    

            # First we two branches for the tagger/jet 
            #  - how far the closest true object was
            #  - and what true_index (i) it had in the list of true objects
            full_i_branch_name =  "jet_{0}__close_{1}_i".format(object_name, particle_name)
            full_dr_branch_name = "jet_{0}__close_{1}_dr".format(object_name, particle_name)

            # Then we build a list of pairs
            # deltaR and jet_index of the jet in ITS list (so we can access it later)
            # the true_index of is only used to filter out jets that are matched to other tops!            
            i_branch = AH.getter(intree, full_i_branch_name)
            dr_branch = AH.getter(intree, full_dr_branch_name)
            dr_and_pos = [(dr,pos) for i,dr,pos in zip(i_branch, dr_branch, range(len(i_branch))) if i==i_particle]

            # Apply the Delta R cut
            dr_and_pos = [(dr,pos) for dr,pos in dr_and_pos if dr < object_drs[object_name]]

            if len(dr_and_pos):
                # Now extract the closest jet and use it to fill the branches
                i_matched = sorted(dr_and_pos, key=lambda x:x[0])[0][1]

                for branch_name in branch_names:
                    full_branch_in  = "jet_{0}__{1}".format(object_name, branch_name)
                    full_branch_out = "{0}_{1}".format(object_name, branch_name)
                    variables[full_branch_out][0] = AH.getter(intree, full_branch_in)[i_matched]                    
            else:
                for branch_name in branch_names:
                    full_branch_out = "{0}_{1}".format(object_name, branch_name)
                    variables[full_branch_out][0] = DEF_VAL_FLOAT

        # Fill the tree
        outtree.Fill()    

    # End of particle loop
# End of Event Loop


# Save everything & exit cleanly
outtree.AutoSave()
outfile.Close()    

