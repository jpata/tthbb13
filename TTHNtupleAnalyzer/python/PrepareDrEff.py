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
    li_htt_branches = ['looseHTT','looseOptRHTT', "msortHTT"] 

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
        
# Truth particle information
particle_branches_float = ["pt", "eta", "phi", "mass"]
particle_branches_int = ["pdgid"]
particle_branches = particle_branches_float + particle_branches_int


# "Normal" branches for most fatjet collections
fj_branches = ["pt", "mass"]


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
li_fatjets = [x for x in li_fatjets if not "cmstt_sj" in x]

# Generic
objects = {}
for fj in li_fatjets:
    print "Adding", fj
    objects[fj] = fj_branches


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

AH.addScalarBranches(variables,
                     variable_types,
                     outtree,
                     ["{0}_{1}".format(particle_name, branch_name) for branch_name in particle_branches_float],
                     datatype = 'float')
AH.addScalarBranches(variables,
                     variable_types,
                     outtree,
                     ["{0}_{1}".format(particle_name, branch_name) for branch_name in particle_branches_int],
                     datatype = 'int')


AH.addScalarBranches(variables, variable_types, outtree,
                     ["top_size", "dr_ca15", "dr_ak08",
                      "b_pt", "b_eta", "b_phi", "b_mass",
                      "w1_pt", "w1_eta", "w1_phi", "w1_mass",
                      "w2_pt", "w2_eta", "w2_phi", "w2_mass"],
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
            b_pt   = AH.getter(intree, "{0}__b__pt".format(true_top_name))
            b_eta  = AH.getter(intree, "{0}__b__eta".format(true_top_name))
            b_phi  = AH.getter(intree, "{0}__b__phi".format(true_top_name))
            b_mass = AH.getter(intree, "{0}__b__mass".format(true_top_name))

            # leading w daughter
            w1_pt   = AH.getter(intree, "{0}__w_d1__pt".format(true_top_name))
            w1_eta  = AH.getter(intree, "{0}__w_d1__eta".format(true_top_name))
            w1_phi  = AH.getter(intree, "{0}__w_d1__phi".format(true_top_name))
            w1_mass = AH.getter(intree, "{0}__w_d1__mass".format(true_top_name))

            # sub-leading w daughter
            w2_pt   = AH.getter(intree, "{0}__w_d2__pt".format(true_top_name))
            w2_eta  = AH.getter(intree, "{0}__w_d2__eta".format(true_top_name))
            w2_phi  = AH.getter(intree, "{0}__w_d2__phi".format(true_top_name))
            w2_mass = AH.getter(intree, "{0}__w_d2__mass".format(true_top_name))

            # Take maximal distance of a decay product to the top as the tops size
            x = deltaR(b_eta, b_phi, variables["hadtop_eta"][0], variables["hadtop_phi"][0])
            y = deltaR(w1_eta, w1_phi, variables["hadtop_eta"][0], variables["hadtop_phi"][0])
            z = deltaR(w2_eta, w2_phi, variables["hadtop_eta"][0], variables["hadtop_phi"][0])

            variables["b_pt"][0]   = b_pt
            variables["b_eta"][0]  = b_eta
            variables["b_phi"][0]  = b_phi
            variables["b_mass"][0] = b_mass

            if w1_pt > w2_pt:
                variables["w1_pt"][0]   = w1_pt
                variables["w1_eta"][0]  = w1_eta
                variables["w1_phi"][0]  = w1_phi
                variables["w1_mass"][0] = w1_mass

                variables["w2_pt"][0]   = w2_pt
                variables["w2_eta"][0]  = w2_eta
                variables["w2_phi"][0]  = w2_phi
                variables["w2_mass"][0] = w2_mass        
            else:
                variables["w1_pt"][0]   = w2_pt
                variables["w1_eta"][0]  = w2_eta
                variables["w1_phi"][0]  = w2_phi
                variables["w1_mass"][0] = w2_mass

                variables["w2_pt"][0]   = w1_pt
                variables["w2_eta"][0]  = w1_eta
                variables["w2_phi"][0]  = w1_phi
                variables["w2_mass"][0] = w1_mass        

            if max([x,y,z]) < 0:
                print x, y, z, max([x,y,z])
                
            variables["top_size"][0] = max([x,y,z])

            i_ca15_branch = AH.getter(intree, "jet_ca15__close_hadtop_i")
            dr_ca15_branch = AH.getter(intree, "jet_ca15__close_hadtop_dr")
            if any([i==i_particle for i in i_ca15_branch]):
                variables["dr_ca15"][0] =  min([dr for i,dr in zip(i_ca15_branch, dr_ca15_branch) if i==i_particle])
            else:
                variables["dr_ca15"][0] = 1000

            i_ak08_branch = AH.getter(intree, "jet_ak08__close_hadtop_i")
            dr_ak08_branch = AH.getter(intree, "jet_ak08__close_hadtop_dr")
            if any([i==i_particle for i in i_ak08_branch]):
                variables["dr_ak08"][0] =  min([dr for i,dr in zip(i_ak08_branch, dr_ak08_branch) if i==i_particle])
            else:
                variables["dr_ak08"][0] = 1000



            # Fill the tree
            outtree.Fill()    

    # End of particle loop


# End of Event Loop

# Save everything & exit cleanly
outtree.AutoSave()
outfile.Close()    

