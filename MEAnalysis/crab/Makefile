all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/V16/ttHTobb_M125_13TeV_powheg_pythia8.dat ttHTobb_M125_13TeV_powheg_pythia8 datasets/ttHTobb_M125_13TeV_powheg_pythia8_1000.dat 1000
	./split.py ../gc/datasets/V16/TT_TuneCUETP8M1_13TeV-powheg-pythia8.dat TT_TuneCUETP8M1_13TeV-powheg-pythia8 datasets/TT_TuneCUETP8M1_13TeV-powheg-pythia8_5000.dat 5000

#make crab configuration files
configs:
	./makeConfigs.py `git rev-parse --short HEAD` datasets/*.dat
