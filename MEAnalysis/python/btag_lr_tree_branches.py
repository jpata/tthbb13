from TTH.TTHNtupleAnalyzer.headergen import *

for b in [
	"permutation_pos",
	"bLep_pos",
	"w1_pos",
	"w2_pos",
	"bHad_pos",
	"b1_pos",
	"jets_bLep_pos",
	"jets_w1_pos",
	"jets_w2_pos",
	"jets_bHad_pos",
	"jets_b1_pos",
	"p_b_bLep",
	"p_b_bHad",
	"p_b_b1",
	"p_j_b1",
	"p_b_b2",
	"p_j_b2",
	"p_j_w1",
	"p_j_w2",
	"hypo",
	"p_pos",
	"p_bb",
	"p_jj",
	]:
	process += [Scalar(b, "float")]

for b in ["event", "syst", "nS", "nB",
	"id_bLep", "id_bHad", "id_b1", "id_b2", "id_w1", "id_w2",
	"permutation", "event_run", "event_lumi", "event_id"
	]:
	process += [Scalar(b, "int")]
