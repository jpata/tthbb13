
#sample vhbb+tthbb file
testfile_vhbb_tthbb=/store/user/jpata/tth/Jun17_leptonic_nome/TT_TuneEE5C_13TeV-powheg-herwigpp/Jun17_leptonic_nome/160617_165529/0000/tree_101.root
DATASETPATH=Jun17_leptonic_nome__TT_TuneEE5C_13TeV-powheg-herwigpp
#testfile_vhbb_tthbb=file:///home/joosep/tth/sw/CMSSW/src/TTH/test.root
test_out_dir=$(CMSSW_BASE)/src/TTH/tests_out

get_testfile:
	xrdcp root://storage01.lcg.cscs.ch//pnfs/lcg.cscs.ch/cms/trivcat/$(testfile_vhbb_tthbb) ./test.root

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
	cd MEAnalysis && TTH_CALCME=0 INPUT_FILE=$(testfile_vhbb_tthbb) ME_CONF=python/cfg_local.py python python/MEAnalysis_heppy.py &> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.log
	sleep 5
	du -csh MEAnalysis/Loop_sample/tree.root &>> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.log
	python -c "import ROOT; f=ROOT.TFile('MEAnalysis/Loop_sample/tree.root'); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.log
	cp MEAnalysis/Loop_sample/tree.root $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.root

test_MEAnalysis_withme: test_mkdir
	rm -Rf MEAnalysis/Loop_*
	cd MEAnalysis && TTH_CALCME=1 INPUT_FILE=$(testfile_vhbb_tthbb) ME_CONF=python/cfg_local.py python python/MEAnalysis_heppy.py &> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.log
	sleep 5
	du -csh MEAnalysis/Loop_sample/tree.root &>> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy_calcME.log
	python -c "import ROOT; f=ROOT.TFile('MEAnalysis/Loop_sample/tree.root'); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/MEAnalysis_MEAnalysis_heppy.log
	cp MEAnalysis/Loop_sample/tree.root $(test_out_dir)/MEAnalysis_MEAnalysis_heppy_calcME.root

test_MELooper: test_mkdir melooper
	cd Plotting && FILE_NAMES=$(testfile_vhbb_tthbb) DATASETPATH=$(DATASETPATH) ./python/makeJobfile.py && ./melooper job.json &> $(test_out_dir)/Plotting_MELooper.log
	sleep 5	
	du -csh Plotting/ControlPlotsSparse.root &>> $(test_out_dir)/Plotting_MELooper.log
	python -c "import ROOT; f=ROOT.TFile('Plotting/ControlPlotsSparse.root'); print f.Get('ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb/sl/sparse').GetEntries()" &>> $(test_out_dir)/Plotting_MELooper.log

test_VHBB: test_mkdir
	rm -Rf $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop* 
	cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/ && python vhbb_combined.py &> $(test_out_dir)/VHBB.log
	cp $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop/tree.root $(test_out_dir)/VHBB.root
	sleep 5
	du -csh $(test_out_dir)/VHBB.root 
	python -c "import ROOT; f=ROOT.TFile('$(test_out_dir)/VHBB.root'); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/VHBB.log

test_VHBB_data: test_mkdir
	rm -Rf $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop* 
	cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/ && python vhbb_combined_data.py &> $(test_out_dir)/VHBB_data.log
	cp $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test/Loop/tree.root $(test_out_dir)/VHBB_data.root
	sleep 5
	du -csh $(test_out_dir)/VHBB_data.root 
	python -c "import ROOT; f=ROOT.TFile('$(test_out_dir)/VHBB_data.root'); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/VHBB_data.log

test_VHBB_MEAnalysis: test_mkdir
	rm -Rf MEAnalysis/Loop_*
	cd MEAnalysis && TTH_CALCME=0 INPUT_FILE=$(test_out_dir)/VHBB.root ME_CONF=python/cfg_local.py python python/MEAnalysis_heppy.py &> $(test_out_dir)/VHBB_MEAnalysis_MEAnalysis_heppy.log

test_MEAnalysis_crab_vhbb: test_mkdir
	egrep -o "file:.*root" MEAnalysis/crab_vhbb/PSet.py
	rm -Rf MEAnalysis/crab_vhbb/Output* 
	cd MEAnalysis/crab_vhbb && ./heppy_crab_script.sh 1 &> $(test_out_dir)/MEAnalysis_crab_vhbb.log
	cp MEAnalysis/crab_vhbb/tree.root $(test_out_dir)/MEAnalysis_crab_vhbb.root
	sleep 5	
	du -csh $(test_out_dir)/MEAnalysis_crab_vhbb.root &>> $(test_out_dir)/MEAnalysis_crab_vhbb.log
	python -c "import ROOT; f=ROOT.TFile('$(test_out_dir)/MEAnalysis_crab_vhbb.root');print f.Get('vhbb/tree').GetEntries(); print f.Get('tree').GetEntries()" &>> $(test_out_dir)/MEAnalysis_crab_vhbb.log

get_hashes:
	cd $(CMSSW_BASE)/src/TTH && echo "tthbb13="`git rev-parse --short HEAD` > $(CMSSW_BASE)/src/TTH/hash
	cd $(CMSSW_BASE)/src/TTH/CommonClassifier && echo "CommonClassifier="`git rev-parse --short HEAD` >> $(CMSSW_BASE)/src/TTH/hash
	cd $(CMSSW_BASE)/src/TTH/MEIntegratorStandalone && echo "MEIntegratorStandalone="`git rev-parse --short HEAD` >> $(CMSSW_BASE)/src/TTH/hash
	cd $(CMSSW_BASE)/src && echo "CMSSW="`git rev-parse --short HEAD` >> $(CMSSW_BASE)/src/TTH/hash

.PHONY: test_mkdir get_hashes
