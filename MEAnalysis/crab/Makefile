all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/V16_newjec/ttHTobb_M125_13TeV_powheg_pythia8.dat datasets/ttHTobb_M125_13TeV_powheg_pythia8.dat 500
	./split.py ../gc/datasets/V16_newjec/TT_TuneCUETP8M1_13TeV-powheg-pythia8.dat datasets/TT_TuneCUETP8M1_13TeV-powheg-pythia8.dat 20000
	./split.py ../gc/datasets/V16_newjec/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.dat datasets/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.dat 5000
	./split.py ../gc/datasets/V16_newjec/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat datasets/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat 5000
	./split.py ../gc/datasets/V16_newjec/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat datasets/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat 5000
	./split.py ../gc/datasets/V16_newjec/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat datasets/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat 5000
	./split.py ../gc/datasets/V16_newjec/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat datasets/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat 5000
	./split.py ../gc/datasets/V16_newjec/ttHToNonbb_M125_13TeV_powheg_pythia8.dat datasets/ttHToNonbb_M125_13TeV_powheg_pythia8.dat 5000
	./split.py ../gc/datasets/V16_newjec/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat datasets/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat 5000
	./split.py ../gc/datasets/V16_newjec/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat datasets/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat 5000
	./split.py ../gc/datasets/V16_newjec/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8.dat datasets/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8.dat 5000
	./split.py ../gc/datasets/V16_newjec/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8.dat datasets/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8.dat 5000
	./split.py ../gc/datasets/V16_newjec/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.dat datasets/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.dat 5000
	./split.py ../gc/datasets/V16_newjec/WW_TuneCUETP8M1_13TeV-pythia8.dat datasets/WW_TuneCUETP8M1_13TeV-pythia8.dat 5000
	./split.py ../gc/datasets/V16_newjec/WZ_TuneCUETP8M1_13TeV-pythia8.dat datasets/WZ_TuneCUETP8M1_13TeV-pythia8.dat 5000
	./split.py ../gc/datasets/V16_newjec/ZZ_TuneCUETP8M1_13TeV-pythia8.dat datasets/ZZ_TuneCUETP8M1_13TeV-pythia8.dat 5000

#make crab configuration files
configs:
	./makeConfigs.py `git rev-parse --short HEAD` datasets/*.dat
