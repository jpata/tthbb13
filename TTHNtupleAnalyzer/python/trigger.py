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
handle  = Handle ("edm::TriggerResults")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label = ("TriggerResults", "", "HLT")

i = 0 
# loop over events
for event in events:
    event.getByLabel (label, handle)
    trigs = handle.product()
    print event._event.id().run(), event._event.id().luminosityBlock(), event._event.id().event()
    names = event._event.triggerNames(trigs)
    for iname in range(names.size()):
        print iname, names.triggerName(iname), trigs.accept(iname)
    i += 1
