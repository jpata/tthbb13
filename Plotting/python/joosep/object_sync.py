import ROOT

ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kError

from TTH.Plotting.joosep.samples import samples_dict

samples = [
    "tth_13TeV_phys14",
    "ttjets_13TeV_phys14",
    #"ttjets_13TeV_phys14_bb", "ttjets_13TeV_phys14_b",
    #"ttjets_13TeV_phys14_cc", "ttjets_13TeV_phys14_ll"
]

for sample in samples:
    print sample
    tf = ROOT.TChain("tree")
    for fn in samples_dict[sample].fileNamesS2:
        tf.AddFile(fn)
    print tf.GetEntries()

    nmax = 10
    for iev in range(nmax):
        tf.GetEntry(iev)
        ev = tf
        print "r l e", ev.run, ev.lumi, ev.evt
        print "nj nt", ev.njets, ev.nBCSVM
        for ij in range(ev.njets):
            print "j", ij, ev.jets_pt[ij], ev.jets_eta[ij], ev.jets_phi[ij], ev.jets_mass[ij], ev.jets_btagCSV[ij]
        print "nl", ev.nleps
        for ij in range(ev.nleps):
            print "l", ij, ev.leps_pt[ij], ev.leps_eta[ij], ev.leps_phi[ij], ev.leps_mass[ij], ev.leps_pdgId[ij]
