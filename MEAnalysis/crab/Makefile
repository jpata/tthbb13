all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/V20/ttHTobb_M125_13TeV_powheg_pythia8.dat datasets/ttHTobb_M125_13TeV_powheg_pythia8.dat 1000
	./split.py ../gc/datasets/V20/ttHToNonbb_M125_13TeV_powheg_pythia8.dat datasets/ttHToNonbb_M125_13TeV_powheg_pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 10000
	./split.py ../gc/datasets/V20/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.dat datasets/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.dat -1
	./split.py ../gc/datasets/V20/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.dat datasets/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1.dat -1
	./split.py ../gc/datasets/V20/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat datasets/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat -1
	./split.py ../gc/datasets/V20/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat datasets/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat -1
	./split.py ../gc/datasets/V20/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat datasets/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat -1
	./split.py ../gc/datasets/V20/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat datasets/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1.dat -1
	./split.py ../gc/datasets/V20/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat datasets/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat datasets/TTWJetsToQQ_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8.dat 10000
	./split.py ../gc/datasets/V20/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8.dat datasets/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8.dat 10000
	./split.py ../gc/datasets/V20/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat -1
	./split.py ../gc/datasets/V20/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat -1
	./split.py ../gc/datasets/V20/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat -1
	./split.py ../gc/datasets/V20/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat -1
	./split.py ../gc/datasets/V20/WW_TuneCUETP8M1_13TeV-pythia8.dat datasets/WW_TuneCUETP8M1_13TeV-pythia8.dat -1
	./split.py ../gc/datasets/V20/WZ_TuneCUETP8M1_13TeV-pythia8.dat datasets/WZ_TuneCUETP8M1_13TeV-pythia8.dat -1
	./split.py ../gc/datasets/V20/ZZ_TuneCUETP8M1_13TeV-pythia8.dat datasets/ZZ_TuneCUETP8M1_13TeV-pythia8.dat -1

#make crab configuration files
configs:
	./makeConfigs.py `git rev-parse --short HEAD` datasets/*.dat
