
#sample vhbb+tthbb file
testfile_vhbb_tthbb=/store/user/jpata/tth/VHBBHeppyV20_tthbbV3_withme_finer/ttHTobb_M125_13TeV_powheg_pythia8/VHBBHeppyV20_tthbbV3_withme_finer_ttHTobb_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160302_131859/0000/tree_885.root
test_out_dir=$(CMSSW_BASE)/src/TTH/tests_out

melooper: Plotting/python/joosep/codeGen.py Plotting/bin/*.cc Plotting/interface/*.h
	cd Plotting && python python/joosep/codeGen.py
	cd Plotting && c++ -g `root-config --cflags --libs` -lPyROOT -I`pwd`/../.. bin/Event.cc bin/MELooper.cc bin/gen.cc bin/categories.cc bin/gason.cpp -o melooper

#This generates the python file which describes the VHBB tree structure
vhbb_wrapper:
	cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test && python genWrapper.py
	cp $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/tree.py $(CMSSW_BASE)/src/TTH/MEAnalysis/python/VHbbTree.py
	git diff --stat $(CMSSW_BASE)/src/TTH/MEAnalysis/python/VHbbTree.py

#This generates the C header file which describes the tthbb tree structure
metree_wrapper:
	cd $(CMSSW_BASE)/src/TTH/MEAnalysis/python && python dumpTree.py && python genWrapper.py tree.json $(CMSSW_BASE)/src/TTH/Plotting/interface/metree.h
	git diff --stat $(CMSSW_BASE)/src/TTH/Plotting/interface/metree.h

#prepares the output directory for the tests
test_mkdir:
	echo $(test_out_dir) && mkdir -p $(test_out_dir)

test_Plotting_makeTF: test_mkdir
	rm -Rf Plotting/python/TransferFunctions/runs/JP_VHBBHeppyV20* 
	cd Plotting/python/TransferFunctions && python cfg_outputtree.py resolvedjets
	cd Plotting/python/TransferFunctions && python cfg_outputtree.py subjets
	cp Plotting/python/TransferFunctions/runs/JP_VHBBHeppyV20/cfg_outputtree.dat Plotting/python/TransferFunctions/
	cd Plotting/python/TransferFunctions && FILE_NAMES=$(testfile_vhbb_tthbb) python outputtree-strict.py &> $(test_out_dir)/Plotting_makeTF.log
	sleep 5 #give time for /shome to catch up
	du -csh Plotting/python/TransferFunctions/out.root &>> $(test_out_dir)/Plotting_makeTF.log
	python -c "import ROOT; f=ROOT.TFile('Plotting/python/TransferFunctions/out.root'); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/Plotting_makeTF.log
	cp Plotting/python/TransferFunctions/out.root $(test_out_dir)/Plotting_makeTF.root

test_Plotting_btaghists: test_mkdir
	cd Plotting/python/joosep/btag && python hists.py test.root $(testfile_vhbb_tthbb)

test_MEAnalysis: test_mkdir
	rm -Rf MEAnalysis/Loop_*
	cd MEAnalysis && ME_CONF=python/cfg_noME.py python python/MEAnalysis_heppy.py &> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.log
	sleep 5
	du -csh MEAnalysis/Loop_ttHTobb_M125_13TeV_powheg_pythia8/tree.root &>> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.log
	python -c "import ROOT; f=ROOT.TFile('MEAnalysis/Loop_ttHTobb_M125_13TeV_powheg_pythia8/tree.root'); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.log
	cp MEAnalysis/Loop_ttHTobb_M125_13TeV_powheg_pythia8/tree.root $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.root

test_MELooper: test_mkdir melooper
	cd Plotting && FILE_NAMES=$(testfile_vhbb_tthbb) DATASETPATH=ttHTobb_M125_13TeV_powheg_pythia8 ./python/makeJobfile.py && ./melooper job.json &> $(test_out_dir)/Plotting_MELooper.log
	sleep 5	
	du -csh Plotting/ControlPlotsSparse.root &>> $(test_out_dir)/Plotting_MELooper.log
	python -c "import ROOT; f=ROOT.TFile('Plotting/ControlPlotsSparse.root'); print f.Get('ttH_hbb/sl/sparse').GetEntries()" &>> $(test_out_dir)/Plotting_MELooper.log

test_VHBB: test_mkdir
	rm -Rf $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop* 
	cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/ && python vhbb_combined.py &> $(test_out_dir)/VHBB.log
	cp $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop/tree.root $(test_out_dir)/VHBB.root
	sleep 5
	du -csh $(test_out_dir)/VHBB.root 
	python -c "import ROOT; f=ROOT.TFile('$(test_out_dir)/VHBB.root'); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/VHBB.log

test_MEAnalysis_crab_vhbb: test_mkdir
	egrep -o "file:.*root" MEAnalysis/crab_vhbb/PSet.py
	rm -Rf MEAnalysis/crab_vhbb/Output* 
	cd MEAnalysis/crab_vhbb && ./heppy_crab_script.sh 1 &> $(test_out_dir)/MEAnalysis_crab_vhbb.log
	cp MEAnalysis/crab_vhbb/tree.root $(test_out_dir)/MEAnalysis_crab_vhbb.root
	sleep 5	
	du -csh $(test_out_dir)/MEAnalysis_crab_vhbb.root &>> $(test_out_dir)/MEAnalysis_crab_vhbb.log
	python -c "import ROOT; f=ROOT.TFile('$(test_out_dir)/MEAnalysis_crab_vhbb.root');print f.Get('vhbb/tree').GetEntries(); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/MEAnalysis_crab_vhbb.log

get_hashes:
	echo "tthbb13="`git rev-parse HEAD` > hash
	cd CommonClassifier && echo "CommonClassifier="`git rev-parse HEAD` >> ../hash
	cd $(CMSSW_BASE)/src && echo "CMSSW="`git rev-parse HEAD` >> TTH/hash

.PHONY: test_mkdir get_hashes
