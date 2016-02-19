all: split configs

#make input datasets for crab
split:
	./split.py ../gc/datasets/V20/ttHTobb_M125_13TeV_powheg_pythia8.dat datasets/ttHTobb_M125_13TeV_powheg_pythia8.dat 5000
	./split.py ../gc/datasets/V20/ttHToNonbb_M125_13TeV_powheg_pythia8.dat datasets/ttHToNonbb_M125_13TeV_powheg_pythia8.dat -1
	./split.py ../gc/datasets/V20/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 20000
	./split.py ../gc/datasets/V20/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 20000
	./split.py ../gc/datasets/V20/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 20000
	./split.py ../gc/datasets/V20/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 20000
	./split.py ../gc/datasets/V20/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 20000
	./split.py ../gc/datasets/V20/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 20000
	./split.py ../gc/datasets/V20/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 20000
	./split.py ../gc/datasets/V20/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat datasets/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.dat 20000

#make crab configuration files
configs:
	./makeConfigs.py `git rev-parse --short HEAD` datasets/*.dat
