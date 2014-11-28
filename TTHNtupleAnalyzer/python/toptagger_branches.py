from TTH.TTHNtupleAnalyzer.headergen import *

# Fatjet Branche
for fj_name in ["fat"]:

    # How many of these objects do we have?
    full_counter_name = "n__jet_{0}".format(fj_name)
    process += [Scalar(full_counter_name, "int")]

    # And all the individual branches
    for branch_name in [
            "pt", "eta", "phi", "mass",  # Kinematics
            "tau1", "tau2", "tau3",  # N-subjettiness
            "close_hadtop_pt",  "close_hadtop_dr"       # truth matching
    ]:     

        full_branch_name = "jet_{0}__{1}".format(fj_name, branch_name)
        process += [Dynamic1DArray(full_branch_name,
                                   "float",
                                   full_counter_name,
                                   "N_MAX"
                               )]

    # End of loop over branches
# End of loop over fat jets


# HEPTopTagger Branches
htt_float_branches =  [
    "pt", "mass", "eta", "phi", "energy",        # Kinematics
    "fj_pt", "fj_mass", "fj_eta", "fj_phi",      # Original Fat-jet kinematics
    "fW", "massRatioPassed",                     # Standard HTT variables
    "Rmin", "ptFiltForRminExp", "RminExpected",  # MultiR variables
    "prunedMass", "topMass", "unfilteredMass",   # extra masses
    "close_hadtop_pt",  "close_hadtop_dr"        # truth matching
]

htt_int_branches = ["child_idx", "isMultiR", "n_sj"]

htt_sj_float_branches =  ["energy", "eta", "mass", "phi", "pt"]

htt_sj_int_branches =  ["parent_idx"]

for htt_name in ["toptagger", "toptagger2"]:

    # How many objects do we have?
    tagger_counter_name = "n__jet_{0}".format(htt_name)
    sj_counter_name = "n__jet_{0}_sj".format(htt_name)
    process += [Scalar(tagger_counter_name, "int")]
    process += [Scalar(sj_counter_name, "int")]

    # Float branches: One per tagger candidate
    for branch_name in htt_float_branches:
        full_branch_name = "jet_{0}__{1}".format(htt_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, "float", tagger_counter_name, "N_MAX")]

    # Int branches: One per tagger candidate
    for branch_name in htt_int_branches:
        full_branch_name = "jet_{0}__{1}".format(htt_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, "int", tagger_counter_name, "N_MAX")]

    # Float branches: One per tagger subjet
    for branch_name in htt_sj_float_branches:
        full_branch_name = "jet_{0}_sj__{1}".format(htt_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, "float", sj_counter_name, "N_MAX")]

    # Int branches: One per tagger subjet
    for branch_name in htt_sj_int_branches:
        full_branch_name = "jet_{0}_sj__{1}".format(htt_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, "int", sj_counter_name, "N_MAX")]

# End of loop over heptoptaggers
