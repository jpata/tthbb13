all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/sig.dat ttHTobb_M125_13TeV_powheg_pythia8 datasets/ttHTobb_M125_13TeV_powheg_pythia8.dat 1000
	./split.py ../gc/datasets/sig.dat ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8 datasets/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8.dat 1000

#make crab configuration files
configs:
	./makeConfigs.py datasets/*.dat
