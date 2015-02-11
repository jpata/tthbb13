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
    from TTH.TTHNtupleAnalyzer.HiggsTaggers_cfg import li_fatjets_branches as higgs_fj_branches
    from TTH.TTHNtupleAnalyzer.Taggers_cfg import li_fatjets_branches as top_fj_branches

# on the Grid
else:
    import AccessHelpers as AH
    
    try:
        from HiggsTaggers_cfg import li_fatjets_branches as higgs_fj_branches
    except:
        higgs_fj_branches = []

    try:
        from Taggers_cfg import li_fatjets_branches as top_fj_branches
    except:
        top_fj_branches = []



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
    particle_name = "hadtop"
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


# Event Info
# Dictionary of event info branches to add
# key -> branch name to use for storing
# value -> list[branch name in input, data type]
event_infos = {"npv" : ["n__pv", "int"]}
        
particle_branches = ["pt", "eta", "phi", "mass"]

# "Normal" branches for most fatjet collections
fj_branches = ["pt", "mass", "tau1", "tau2", "tau3"]

# Extended fj branches, including
#   shower deconstruction chi
#   qjets volatility
# (to expensive to calc for everything)
fj_branches_plus = fj_branches + ["chi", "qvol", "nmj"]

htt_branches = ["pt", "mass", "fW", "Rmin", "RminExpected", "prunedMass", "ptFiltForRminExp"]
cmstt_branches = ["pt", "mass", "minMass", "wMass", "topMass", "nSubJets"]

li_fatjets = higgs_fj_branches + top_fj_branches + ['ca08', 'ca15', 'ca08puppi', 'ca15puppi', 'ca08trimmedr2f6', 'ca08trimmedr2f10', 'ca08softdropz15b00', 'ca08softdropz20b10', 'ca08softdropz30b10', 'ca08softdropz30b15', 'ca15trimmedr2f6', 'ca15trimmedr2f10', 'ca15softdropz15b00', 'ca15softdropz20b10', 'ca15softdropz30b10', 'ca15softdropz30b15', 'ca08puppitrimmedr2f6', 'ca08puppitrimmedr2f10', 'ca08puppisoftdropz15b00', 'ca08puppisoftdropz20b10', 'ca08puppisoftdropz30b10', 'ca08puppisoftdropz30b15', 'ca15puppitrimmedr2f6', 'ca15puppitrimmedr2f10', 'ca15puppisoftdropz15b00', 'ca15puppisoftdropz20b10', 'ca15puppisoftdropz30b10', 'ca15puppisoftdropz30b15']


# Generic
objects = {}
for fj in li_fatjets:
    objects[fj] = fj_branches

# And some extras
objects["ca08"]                = fj_branches_plus
objects["ca15"]                = fj_branches_plus
objects["ca08puppi"]           = fj_branches_plus
objects["ca15puppi"]           = fj_branches_plus
objects["ca08cmstt"]           = cmstt_branches
objects["ca15cmstt"]           = cmstt_branches
objects["ca08puppicmstt"]      = cmstt_branches
objects["ca15puppicmstt"]      = cmstt_branches
objects["looseMultiRHTT"]      = htt_branches
objects["looseMultiRHTTpuppi"] = htt_branches


# Matching DeltaR for the varipus object types
object_drs = {}                      
for object_name in objects.keys():
    if "ca08" in object_name:
        object_drs[object_name] = 0.6
    elif "ca15" in object_name:
        object_drs[object_name] = 1.2
    elif "looseMultiRHTT" in object_name:
        object_drs[object_name] = 1.2
    else:
        print "No delta R defined for", object_name
        print "Exiting!"
        sys.exit()



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

# Setup branch for distance jet-truth particle
AH.addScalarBranches(variables, variable_types, outtree, ["dr"], datatype = 'float')

# Setup the output branches for the event info
for k,v in event_infos.iteritems():
    AH.addScalarBranches(variables,
                         variable_types,
                         outtree,
                         [k],
                         datatype = v[1])

# Setup the output branches for the true object
AH.addScalarBranches(variables,
                     variable_types,
                     outtree,
                     ["{0}_{1}".format(particle_name, branch_name) for branch_name in particle_branches],
                     datatype = 'float')

# Setup the output branches for tagging variables
objects_to_pop = []
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
            objects_to_pop.append(object_name)
# End of loop over objects and branches

objects_to_pop = list(set(objects_to_pop))
for o in objects_to_pop:
    objects.pop(o)

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

        # Fill Event Info Branches
        for k,v in event_infos.iteritems():            
            variables[k][0] = AH.getter(intree, v[0])
            

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
                closest_dr_and_pos = sorted(dr_and_pos, key=lambda x:x[0])[0]
                i_matched = closest_dr_and_pos[1]

                variables["dr"][0] = closest_dr_and_pos[0]
                for branch_name in branch_names:
                    full_branch_in  = "jet_{0}__{1}".format(object_name, branch_name)
                    full_branch_out = "{0}_{1}".format(object_name, branch_name)
                    variables[full_branch_out][0] = AH.getter(intree, full_branch_in)[i_matched]                    
            else:
                variables["dr"][0] = 9999.
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

