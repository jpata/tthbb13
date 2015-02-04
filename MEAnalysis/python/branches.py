#branch file for METree.hh

#uses branch classes from headergen
from TTH.TTHNtupleAnalyzer.headergen import *

#uses toptagger branches
from TTH.TTHNtupleAnalyzer.toptagger_branches import *

#notify headergen that we want to copy the branches from the input tree to the output tree
for b in process:
	b.needs_copy = True

#for x in ["pt", "eta", "phi", "m", "id"]:
#	process += [Dynamic1DArray("gen_lepton_{0}".format(x), "float", "nLep", "NMAXLEPTONS")]
#	process += [Dynamic1DArray("gen_jet_{0}".format(x), "float", "nJet", "NMAXLEPTONS")]
process += [Scalar("mW", "float")]
process += [Scalar("selected_comb", "int")]
process += [Static1DArray("pos_to_index", "int", 6)]
process += [
	Scalar("btag_LR", "float"),
	Scalar("btag_LR2", "float"),
	Scalar("btag_LR3", "float"),
	Scalar("btag_LR4", "float"),
	Scalar("btag_lr_l_bbbb", "float"),
	Scalar("btag_lr_l_bbcc", "float"),
	Scalar("btag_lr_l_bbjj", "float"),
	Scalar("btag_lr_l_bbbbcq", "float"),
	Scalar("btag_lr_l_bbcccq", "float"),
	Scalar("btag_lr_l_bbjjcq", "float")
]
