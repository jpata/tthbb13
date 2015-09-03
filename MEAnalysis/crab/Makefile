all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/sig.dat ttHTobb_M125_13TeV_powheg_pythia8 datasets/ttHTobb_M125_13TeV_powheg_pythia8.dat 1000
	./split.py ../gc/datasets/bkg.dat TT_TuneCUETP8M1_13TeV-powheg-pythia8 datasets/TT_TuneCUETP8M1_13TeV-powheg-pythia8.dat 5000

#make crab configuration files
configs:
	./makeConfigs.py datasets/*.dat
