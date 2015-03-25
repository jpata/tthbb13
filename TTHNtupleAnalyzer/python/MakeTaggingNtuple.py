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
import math
import socket

import ROOT

# for working on tier 3
if socket.gethostname() == "t3ui12":
    import TTH.TTHNtupleAnalyzer.AccessHelpers as AH
    from TTH.TTHNtupleAnalyzer.Taggers_cfg import li_htt_branches

# on the Grid
else:
    import AccessHelpers as AH

    try:
        from Taggers_cfg import li_htt_branches
    except:
        li_htt_branches = []

########################################
# deltaR
########################################

def deltaR(eta1, phi1, eta2, phi2):
    """ Helper function to calculate delta R"""
    tlv1 = ROOT.TLorentzVector()
    tlv2 = ROOT.TLorentzVector()
    
    tlv1.SetPtEtaPhiM(1, eta1, phi1, 0)
    tlv2.SetPtEtaPhiM(1, eta2, phi2, 0)

    dphi = abs(abs(abs(phi1-phi2)-math.pi)-math.pi)
    deta = eta1 - eta2

    return math.sqrt(pow(dphi,2) + pow(deta,2))


def deltaRAlt(eta1, phi1, eta2, phi2):
    """ Helper function to calculate delta R
    Alternative version using TLorentzVector    
    """
    tlv1 = ROOT.TLorentzVector()
    tlv2 = ROOT.TLorentzVector()
    
    tlv1.SetPtEtaPhiM(1, eta1, phi1, 0)
    tlv2.SetPtEtaPhiM(1, eta2, phi2, 0)

    return tlv1.DeltaR(tlv2)



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
    elif ("TTbarH_HToBB_M" in initial_miniAOD_filename or 
          "Rad_HHto4b" in initial_miniAOD_filename):
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

fj_branches_btag = fj_branches + ["btag"]

htt_branches = ["pt", "mass", "fW", "Rmin", "RminExpected", "prunedMass", "ptFiltForRminExp"]
cmstt_branches = ["pt", "mass", "minMass", "wMass", "topMass", "nSubJets"]




li_htt_branches = li_htt_branches + ['looseMultiRHTT']#'softdropz20b10MultiRHTT', 'softdropz15bminus20MultiRHTT', 'softdropz15bminus10MultiRHTT', 'softdropz15b00MultiRHTT', 'softdropz15b10MultiRHTT', 'looseMultiRHTTpuppi', 'softdropz20b10MultiRHTTpuppi', 'softdropz15bminus20MultiRHTTpuppi', 'softdropz15bminus10MultiRHTTpuppi', 'softdropz15b00MultiRHTTpuppi', 'softdropz15b10MultiRHTTpuppi']




########################################
# Prepare input/output
########################################

infile = ROOT.TFile(infile_name)
intree = infile.Get('tthNtupleAnalyzer/events')

branches_in_input = [b.GetName() for b in intree.GetListOfBranches()]

li_fatjets =  [b.replace("jet_","") for b in branches_in_input if len(b.split("__")) > 1 and b.split("__")[1] == "pt" and b.split("_")[0]=="jet"]
li_fatjets = [b.replace("__pt","") for b in li_fatjets]
if '_pt' in li_fatjets:
    li_fatjets.remove("_pt")


# Generic
objects = {}
for fj in li_fatjets:
    objects[fj] = fj_branches
    
# HEPTopTagger
for htt in li_htt_branches:
    objects[htt]                = htt_branches

# And some extras
for x in ["ca08", "ca15", "ca08puppi", "ca15puppi"]:
    if x in objects.keys():
        objects[x] = fj_branches_plus

for x in ["ca08cmstt", "ca15cmstt", "ca08puppicmstt", "ca15puppicmstt"]:
    if x in objects.keys():
        objects[x] = cmstt_branches

# Subjet b-tagging
for k,v in objects.iteritems():
    if "forbtag" in k:
        objects[k] = fj_branches_btag



# Matching DeltaR for the varipus object types
object_drs = {}                      
for object_name in objects.keys():
    if "ca08" in object_name:
        object_drs[object_name] = 0.6
    elif "ca15" in object_name:
        object_drs[object_name] = 1.2
    elif "HTT" in object_name:
        object_drs[object_name] = 1.2
    else:
        print "No delta R defined for", object_name
        print "Exiting!"
        sys.exit()





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

AH.addScalarBranches(variables, variable_types, outtree,
                     ["top_size"],
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
            print "Warning: Branch {0} not available in input file. Removing  {1}".format(full_branch_in, object_name)
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

        # If we have the hadronic top, we also want to know it's size
        # This is a bit tricky as we only store the decay products for top and antitop
        # so first we check which one of the two our hadronic top actually was
        # and then we look at the daughters of that object
        if particle_name == "hadtop":
            t_eta = AH.getter(intree, "gen_t__eta")
            t_phi = AH.getter(intree, "gen_t__phi")
            tbar_eta = AH.getter(intree, "gen_tbar__eta")
            tbar_phi = AH.getter(intree, "gen_tbar__phi")
            
            dr_had_t    = deltaR(variables["hadtop_eta"][0], variables["hadtop_phi"][0], t_eta, t_phi)  
            dr_had_tbar = deltaR(variables["hadtop_eta"][0], variables["hadtop_phi"][0], tbar_eta, tbar_phi) 
            
            if dr_had_t < dr_had_tbar:
                true_top_name = "gen_t"
            else:
                true_top_name = "gen_tbar"
        
            # b-quark
            b_eta = AH.getter(intree, "{0}__b__eta".format(true_top_name))
            b_phi = AH.getter(intree, "{0}__b__phi".format(true_top_name))
            # leading w daughter
            w1_eta = AH.getter(intree, "{0}__w_d1__eta".format(true_top_name))
            w1_phi = AH.getter(intree, "{0}__w_d1__phi".format(true_top_name))
            # sub-leading w daughter
            w2_eta = AH.getter(intree, "{0}__w_d2__eta".format(true_top_name))
            w2_phi = AH.getter(intree, "{0}__w_d2__phi".format(true_top_name))

            # Take maximal distance of a decay product to the top as the tops size
            x = deltaR(b_eta, b_phi, variables["hadtop_eta"][0], variables["hadtop_phi"][0])
            y = deltaR(w1_eta, w1_phi, variables["hadtop_eta"][0], variables["hadtop_phi"][0])
            z = deltaR(w2_eta, w2_phi, variables["hadtop_eta"][0], variables["hadtop_phi"][0])
                        
            top_size = max([x,y,z])
        else:
            top_size = -1
        variables["top_size"][0] = top_size
            
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

            
            # Special treatment for b-tagging subjets. Don't take closest but b-likeliest in radius
            if "forbtag" in object_name:
                
                full_btag_branch_name = "jet_{0}__btag".format(object_name)
                btag_branch = AH.getter(intree, full_btag_branch_name)

                
                dr_pos_btag = [(dr,pos,btag) for i,dr,btag,pos in zip(i_branch, dr_branch, btag_branch, range(len(i_branch))) if i==i_particle]

                # Apply the Delta R cut
                dr_pos_btag = [(dr,pos,btag) for dr,pos,btag in dr_pos_btag if dr < object_drs[object_name]]

                if len(dr_pos_btag):

                    # Now extract the highest b-tag scored jet and use it to fill the branches
                    closest_dr_pos_btag = sorted(dr_pos_btag, key=lambda x:x[2])[-1]
                    i_matched = closest_dr_pos_btag[1]

                    variables["dr"][0] = closest_dr_pos_btag[0]
                    for branch_name in branch_names:
                        full_branch_in  = "jet_{0}__{1}".format(object_name, branch_name)
                        full_branch_out = "{0}_{1}".format(object_name, branch_name)
                        variables[full_branch_out][0] = AH.getter(intree, full_branch_in)[i_matched]                    
                else:
                    variables["dr"][0] = 9999.
                    for branch_name in branch_names:
                        full_branch_out = "{0}_{1}".format(object_name, branch_name)
                        variables[full_branch_out][0] = DEF_VAL_FLOAT
            # Done handling b-tagged subjets

            else:
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

        # end of loop over objects

        # Fill the tree
        outtree.Fill()    

    # End of particle loop
# End of Event Loop

# Save everything & exit cleanly
outtree.AutoSave()
outfile.Close()    

