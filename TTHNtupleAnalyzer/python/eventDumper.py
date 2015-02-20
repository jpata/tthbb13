import ROOT, sys
from DataFormats.FWLite import Events, Handle

events = Events(sys.argv[1])

jets_handle = Handle('std::vector<pat::Jet>')
jets_label = ("slimmedJets")
ROOT.gROOT.SetBatch()

for event in events:
	event.getByLabel(jets_label, jets_handle)
	jets = jets_handle.product()
	for jet in jets:
		print jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.pdgId()
