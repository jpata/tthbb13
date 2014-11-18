#sample branches file for headergen.py
#uses branch classes from headergen
from TTH.TTHNtupleAnalyzer.headergen import *

#define branches to add here
process = [
	Scalar("gen_t__dpt_alt", "float"),
	Scalar("gen_tbar__dpt_alt", "float"),
	#Dynamic1DArray("fjet__pt", "float", "n__fjet", "N_FATJETS"),
	#Dynamic1DArray("fjet__eta", "float", "n__fjet", "N_FATJETS"),
	#Static1DArray("jec", "float", "NJECS")
]

# True Top Branches
for t in ["t2", "tbar2"]:
    for v in [
        ("b__eta"), ("b__mass"), ("b__phi"), ("b__pt"), ("b__status"),
        ("w_d1__eta"), ("w_d1__mass"), ("w_d1__phi"), ("w_d1__pt"), ("w_d1__status"),
        ("w_d2__eta"), ("w_d2__mass"), ("w_d2__phi"), ("w_d2__pt"), ("w_d2__status")
    ]:
        typ = "float"
        if "status" in v or "id" in v:
            typ = "int"
        process += [Scalar("gen_%s__%s" % (t, v), typ)]


# Fatjet Branches
for fj_name in ["fat"]:

    # How many of these objects do we have?
    full_counter_name = "n__jet_{0}".format(fj_name)
    process += [Scalar(full_counter_name, "int")]

    # And all the individual branches
    for branch_name in [
            "pt", "eta", "phi", "mass",  # Kinematics
            "tau1", "tau2", "tau3"]:     # N-subjettiness

        full_branch_name = "jet_{0}__{1}".format(fj_name, branch_name)
        process += [Dynamic1DArray(full_branch_name, 
                                   "float",
                                   full_counter_name,
                                   "N_MAX"
                               )]

    # End of loop over branches
# End of loop over fat jets
