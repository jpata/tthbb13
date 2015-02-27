import ROOT, sys
from DataFormats.FWLite import Events, Handle

events = Events(sys.argv[1])

jets_handle = Handle('std::vector<pat::Jet>')
jets_label = ("slimmedJets")

pf_handle = Handle('std::vector<pat::PackedCandidate>')
pf_label = ("packedPFCandidates")

ROOT.gROOT.SetBatch()

for event in events:
    ids = event.eventAuxiliary().id().run(), event.eventAuxiliary().id().luminosityBlock(), event.eventAuxiliary().id().event()
    event.getByLabel(jets_label, jets_handle)
    jets = jets_handle.product()
    for nj, jet in enumerate(jets):
        print "jet", ids[0], ids[1], ids[2], nj, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.pdgId()
    event.getByLabel(pf_label, pf_handle)
    pfs = pf_handle.product()
    for n, pf in enumerate(pfs):
        print "pfc", ids[0], ids[1], ids[2], n, pf.pt(), pf.eta(), pf.phi(), pf.mass(), pf.pdgId()

