#sample branches file for headergen.py
#uses branch classes from headergen
from TTH.TTHNtupleAnalyzer.headergen import *
from TTH.TTHNtupleAnalyzer.Taggers_cfg import li_fatjets_branches, li_ungroomed_fatjets_branches, li_htt_branches

defines.extend(["#define ADD_TRUE_TOP_MATCHING_FOR_FJ 1",
                "#define ADD_TRUE_TOP_MATCHING_FOR_HTT 1",
                "#define ADD_TRUE_TOP_MATCHING_FOR_CMSTT 1",
                "#define ADD_TRUE_HIGGS_MATCHING_FOR_FJ 1",
                "#define ADD_TRUE_HIGGS_MATCHING_FOR_HTT 1",
                "#define ADD_TRUE_HIGGS_MATCHING_FOR_CMSTT 1",
                "#define ADD_TRUE_PARTON_MATCHING_FOR_FJ 1",
                "#define ADD_TRUE_PARTON_MATCHING_FOR_HTT 1",
                "#define ADD_TRUE_PARTON_MATCHING_FOR_CMSTT 1"])


#define branches to add here
process = [
	Scalar("gen_t__dpt_alt", "float"),
	Scalar("gen_tbar__dpt_alt", "float"),
]


process += Scalar("weight__genmc", "float"),

# Simple Truth Branches
# - Just the kinematics
# - above a pT threshold
# - these are the objects the jets/taggers are matched to and know the indices of
for particle in ["hadtop", "higgs", "parton"]:

    counter_name =  "n__gen_{0}".format(particle)
    process += [Scalar(counter_name, "int")]

    for v in ["eta", "mass", "phi", "pt"]:
        full_branch_name = "gen_{0}__{1}".format(particle, v)
        process += [Dynamic1DArray(full_branch_name, "float", counter_name, "N_MAX")]

    for v in ["pdgid"]:
        full_branch_name = "gen_{0}__{1}".format(particle, v)
        process += [Dynamic1DArray(full_branch_name, "int", counter_name, "N_MAX")]
# End of Simple Truth


# True Top Branches
for t in ["t", "tbar", "t2", "tbar2"]:
    for v in [
        ("eta"), ("mass"), ("phi"), ("pt"), ("status"),
        ("b__eta"), ("b__mass"), ("b__phi"), ("b__pt"), ("b__status"),
        ("w_d1__eta"), ("w_d1__mass"), ("w_d1__phi"), ("w_d1__pt"), ("w_d1__status"), ("w_d1__id"),
        ("w_d2__eta"), ("w_d2__mass"), ("w_d2__phi"), ("w_d2__pt"), ("w_d2__status"), ("w_d2__id")
    ]:
        typ = "float"
        if "status" in v or "id" in v:
            typ = "int"
        process += [Scalar("gen_%s__%s" % (t, v), typ)]

# True Top Branches
for t in ["b", "bbar"]:
    for v in ["eta", "mass", "phi", "pt", "status", "id"]:
        typ = "float"
        if "status" in v or "id" in v:
            typ = "int"
        process += [Scalar("gen_%s__%s" % (t, v), typ)]







# Fatjet Branches
for fj_name in li_fatjets_branches:

    # How many of these objects do we have?
    full_counter_name = "n__jet_{0}".format(fj_name)
    process += [Scalar(full_counter_name, "int")]

    # And all the individual float branches
    for branch_name in [
            "pt", "eta", "phi", "mass",  # Kinematics
            "tau1", "tau2", "tau3",      # N-subjettiness
            "btag",                      # b-tag discriminator
            "chi1", "nmj1",                # Shower deconstruction chi and number of microjets
                                         # (only fill for ungroomed)
            "chi2", "nmj2",
            "chi3", "nmj3",
            "qvol",                      # Qjet volatility
                                         # (only fill for ungroomed)
            "nconst", "ncharged", "nneutral", # constituent counts
            "hadflavour", "partflavour",
            "close_hadtop_pt",  "close_hadtop_dr", "close_hadtop_i", # top truth matching
            "close_parton_pt",  "close_parton_dr", "close_parton_i", # parton truth matching
            "close_higgs_pt",   "close_higgs_dr",  "close_higgs_i"   # higgs truth matching
            ]:

        # Don't do chi unless we have the unfiltered fatjets
        if (branch_name in ["chi", "nmj"]) and not (fj_name in li_ungroomed_fatjets_branches):
            continue

        if branch_name in ["close_higgs_i", "close_hadtop_i", "close_parton_i", "nmj", "nconst", "ncharged", "nneutral"]:
            the_type = "int"
        else:
            the_type = "float"

        full_branch_name = "jet_{0}__{1}".format(fj_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, 
                                   the_type,
                                   full_counter_name,
                                   "N_MAX"
                               )]

    # End of loop over branches
# End of loop over fat jets


# HEPTopTagger Branches
htt_float_branches =  [
    "pt", "mass", "eta", "phi", "energy",       # Kinematics
    "fj_pt", "fj_mass", "fj_eta", "fj_phi",     # Original Fat-jet kinematics
    "fRec", "massRatioPassed",                  # Standard HTT variables 
    "Ropt", "ptForRoptCalc", "RoptCalc",        # Optimal R variables
    "tau1unfilt", "tau2unfilt", "tau3unfilt",   # Unfiltered N-Subjettiness
    "tau1filt", "tau2filt", "tau3filt",         # Filtered N-Subjettiness
    "qweight", "qepsilon", "qsigmam",           # Q-jet variables
    "prunedMass", "topMass", "unfilteredMass",  # extra masses
    "close_hadtop_pt", "close_hadtop_dr",       # top truth matching
    "close_parton_pt", "close_parton_dr",       # parton truth matching
    "close_higgs_pt",  "close_higgs_dr",        # higgs truth matching
]

htt_int_branches = ["child_idx", "isMultiR", "n_sj", "close_higgs_i", "close_parton_i", "close_hadtop_i"]

htt_sj_float_branches =  ["energy", "eta", "mass", "phi", "pt"]

htt_sj_int_branches =  ["parent_idx"]

for htt_name in li_htt_branches:

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



# CMS TopTagger Branches
cmstt_float_branches =  [
    "pt", "mass", "eta", "phi", "energy",     # Kinematics
    "minMass", "wMass", "topMass",            # Standard CMSTT variables     
    "close_hadtop_pt",  "close_hadtop_dr",    # top truth matching
    "close_parton_pt",  "close_parton_dr",    # parton truth matching
    "close_higgs_pt",   "close_higgs_dr",     # higgs truth matching    
]

cmstt_int_branches = ["child_idx", "nSubJets", "close_higgs_i", "close_parton_i", "close_hadtop_i"]

cmstt_sj_float_branches =  ["energy", "eta", "mass", "phi", "pt", "btag"]

cmstt_sj_int_branches =  ["parent_idx"]

for cmstt_name in ["ak08cmstt", "ca15cmstt", "ak08puppicmstt", "ca15puppicmstt"]:

    # How many objects do we have?
    tagger_counter_name = "n__jet_{0}".format(cmstt_name)
    sj_counter_name = "n__jet_{0}_sj".format(cmstt_name)
    process += [Scalar(tagger_counter_name, "int")]
    process += [Scalar(sj_counter_name, "int")]

    # Float branches: One per tagger candidate
    for branch_name in cmstt_float_branches:
        full_branch_name = "jet_{0}__{1}".format(cmstt_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, "float", tagger_counter_name, "N_MAX")]

    # Int branches: One per tagger candidate
    for branch_name in cmstt_int_branches:
        full_branch_name = "jet_{0}__{1}".format(cmstt_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, "int", tagger_counter_name, "N_MAX")]

    # Float branches: One per tagger subjet
    for branch_name in cmstt_sj_float_branches:
        full_branch_name = "jet_{0}_sj__{1}".format(cmstt_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, "float", sj_counter_name, "N_MAX")]

    # Int branches: One per tagger subjet
    for branch_name in cmstt_sj_int_branches:
        full_branch_name = "jet_{0}_sj__{1}".format(cmstt_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, "int", sj_counter_name, "N_MAX")]

# End of loop over cmstoptaggers







