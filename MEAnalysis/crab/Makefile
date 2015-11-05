all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/V14/ttHTobb_M125_13TeV_powheg_pythia8.dat ttHTobb_M125_13TeV_powheg_pythia8 datasets/ttHTobb_M125_13TeV_powheg_pythia8_2000.dat 2000
	./split.py ../gc/datasets/V14/TT_TuneCUETP8M1_13TeV-powheg-pythia8.dat TT_TuneCUETP8M1_13TeV-powheg-pythia8 datasets/TT_TuneCUETP8M1_13TeV-powheg-pythia8_10000.dat 10000

#make crab configuration files
configs:
	./makeConfigs.py `git rev-parse --short HEAD` datasets/*.dat
