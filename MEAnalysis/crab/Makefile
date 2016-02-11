all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/V16_newjec/ttHTobb_M125_13TeV_powheg_pythia8.dat ttHTobb_M125_13TeV_powheg_pythia8 datasets/ttHTobb_M125_13TeV_powheg_pythia8__N100000.dat 100000
	./split.py ../gc/datasets/V16_newjec/ttHTobb_M125_13TeV_powheg_pythia8.dat ttHTobb_M125_13TeV_powheg_pythia8 datasets/ttHTobb_M125_13TeV_powheg_pythia8__N500.dat 500
	./split.py ../gc/datasets/V16_newjec/TT_TuneCUETP8M1_13TeV-powheg-pythia8.dat TT_TuneCUETP8M1_13TeV-powheg-pythia8 datasets/TT_TuneCUETP8M1_13TeV-powheg-pythia8__N100000.dat 100000
	./split.py ../gc/datasets/V16_newjec/TT_TuneCUETP8M1_13TeV-powheg-pythia8.dat TT_TuneCUETP8M1_13TeV-powheg-pythia8 datasets/TT_TuneCUETP8M1_13TeV-powheg-pythia8__N10000.dat 10000

#make crab configuration files
configs:
	./makeConfigs.py `git rev-parse --short HEAD` datasets/*.dat
