from headergen import *
#add additional defines
defines.extend([])

#add a scalar branch
process += [Scalar(k, "long") for k in ["run", "event", "lumi"]]

process += [Scalar("nleps", "int"), Scalar("njets", "int")]
process += [Scalar("hypothesis", "int"), Scalar("numcalls", "int"), Scalar("systematic", "int")]

process += [Scalar("met_pt", "float"), Scalar("met_phi", "float")]

max_leps = 2
process += [
    Dynamic1DArray("lep_{0}".format(x), "float", "nleps", max_leps)
    for x in ["pt", "eta", "phi", "mass", "charge"]
]

max_jets = 10
process += [
    Dynamic1DArray("jet_{0}".format(x), "float", "njets", max_jets)
    for x in ["pt", "eta", "phi", "mass", "csv", "cmva"]
]

process += [
    Dynamic1DArray("jet_{0}".format(x), "int", "njets", max_jets)
    for x in ["type"]
]
