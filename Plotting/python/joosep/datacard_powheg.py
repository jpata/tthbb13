from datacard import Datacard

#Enable the plotting of these samples
Datacard.samples = [
    "ttHTobb_M125_13TeV_powheg_pythia8_hbb",
    #"ttHTobb_M125_13TeV_powheg_pythia8_hX",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_tt2b",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttb",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttbb",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttcc",
    "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ttll",
]

Datacard.output_filename = "ControlPlots_powheg.root"
