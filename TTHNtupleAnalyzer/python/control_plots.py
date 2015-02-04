import ROOT, numpy

def control_plots(in_filenames, out_filename):
	tt = ROOT.TChain("tthNtupleAnalyzer/events")
	for f in in_filenames:
		tt.AddFile(f, -1)

	print tt.GetEntries()
	for h in range(10):
		print "hypo", h, tt.GetEntries("hypo1 == {0}".format(h))

	of = ROOT.TFile(out_filename, "RECREATE")
	of.cd()
	h_njets = ROOT.TH1D("h_njets", "Number of jets", 15, 0, 15)
	h_njets_ntags = ROOT.TH2D("h_njets_ntags", "Number of jets vs. number of CSVM tags", 15, 0, 15, 15, 0, 15)

	def create_branch(chain, branchname, typ, n):
		arr = numpy.zeros(n, dtype=typ)
		return arr

	a_njets = create_branch(tt, "n__jet", "int32", 1)
	a_jet__pt = create_branch(tt, "jet__pt", "float32", 500)
	a_jet__eta = create_branch(tt, "jet__eta", "float32", 500)
	a_jet__csv = create_branch(tt, "jet__bd_csv", "float32", 500)

	for ev in range(tt.GetEntries()):

		tt.GetEntry(ev)
		nj = a_njets[0]

		njets = 0
		ntags = 0
		for _nj in range(nj):
			pt = a_jet__pt[_nj]
			eta = a_jet__eta[_nj]
			csv = a_jet__csv[_nj]
			if pt>30 and abs(eta)<2.5:
				njets += 1
				if csv > 0.679:
					ntags += 1
		h_njets.Fill(njets)
		h_njets_ntags.Fill(njets, ntags)

	of.Write()
	of.Close()

if __name__ == "__main__":
	control_plots(
		["/hdfs/cms/store/user/jpata/tth/dec19_5b21f5f/TTHbb_s1_5b21f5f_tth_hbb_13tev.root"], "control/dec19_5b21f5f/tth_hbb_13tev.root",
	)

	control_plots(
		["/hdfs/cms/store/user/jpata/tth/jan28_8a4239/TTHbb_s1_8a4239_tth_hbb_13tev_pu20bx25_phys14.root"], "control/jan28_8a4239/tth_hbb_13tev_pu20bx25_phys14.root"
	)
