import ROOT
import sys
from DataFormats.FWLite import Events, Handle

# Make VarParsing object
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.parseArguments()

# use Varparsing object
events = Events (options)

# create handle outside of loop
handle  = Handle ("std::vector<pat::Jet>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label = ("slimmedJets")

bdiscs = [
    "pfCombinedInclusiveSecondaryVertexV2BJetTags",
    "pfCombinedSecondaryVertexV2BJetTags",
]

i = 0 
# loop over events
for event in events:
    event.getByLabel (label, handle)
    jets = handle.product()
    for jet in jets:
        bvals = {}
        print jet.pt()
        for bdisc in bdiscs:
            bvals[bdisc] = jet.bDiscriminator(bdisc)
            if bvals[bdisc]>1:
                print "***", bvals[bdisc]
        #print jet.partonFlavour(), bvals
    i += 1
