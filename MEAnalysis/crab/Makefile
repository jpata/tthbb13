all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/V14/ttHTobb_M125_13TeV_powheg_pythia8.dat ttHTobb_M125_13TeV_powheg_pythia8 datasets/ttHTobb_M125_13TeV_powheg_pythia8_500.dat 500
	./split.py ../gc/datasets/V14/ttHTobb_M125_13TeV_powheg_pythia8.dat ttHTobb_M125_13TeV_powheg_pythia8 datasets/ttHTobb_M125_13TeV_powheg_pythia8_1000.dat 1000

#make crab configuration files
configs:
	./makeConfigs.py `git rev-parse --short HEAD` datasets/*.dat
