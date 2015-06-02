#sample branches file for headergen.py
#uses branch classes from headergen
from headergen import *

#add additional defines
defines.extend([])

#add a scalar branch
process += Scalar("weight__genmc", "float"),

#add vector branches
for t in ["pt", "eta", "phi", "pass"]:
    for x in ["lep", "jet"]:
        full_branch_name = "trig_{0}__{1}".format(x, t)
        process += [
            Dynamic1DArray(full_branch_name, "int" if t=="pass" else "float", "n__{0}".format(x), "N_MAX")
        ]

