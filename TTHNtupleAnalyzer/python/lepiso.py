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
handle  = Handle ("std::vector<pat::Electron>")
rhoHandle  = Handle ("double")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label = ("slimmedElectrons")
rhoLabel = ("fixedGridRhoFastjetAll")

i = 0 
# loop over events
for event in events:
    event.getByLabel (label, handle)
    event.getByLabel (rhoLabel, rhoHandle)
    objs = handle.product()
    rhos = rhoHandle.product()
    print "rho=", float(rhos[0])
    for obj in objs:
        chHadPt = obj.pfIsolationVariables().sumChargedHadronPt
        neHadEt = obj.pfIsolationVariables().sumNeutralHadronEt
        phEt = obj.pfIsolationVariables().sumPhotonEt
        print obj.pt(), obj.eta(), chHadPt, neHadEt, phEt
    i += 1
