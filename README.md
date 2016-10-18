# TTHBB MEM code

Setup on SLC6 in a clean directory (no CMSSW) on a **shared file system**
~~~
$ mkdir -p ~/tth/sw
$ cd ~/tth/sw
$ wget --no-check-certificate https://raw.githubusercontent.com/jpata/tthbb13/meanalysis-80x/setup.sh
$ source setup.sh
~~~
This will download CMSSW, the tthbb code and all the dependencies.

In order to compile the code, run
~~~
$ cd ~/tth/sw/CMSSW/src
$ cmsenv
$ scram b -j 8
~~~

Note that if you run `scram b clean`, the matrix element library OpennLoops will be deleted from CMSSW, which will result in errors like
~~~
[OpenLoops] ERROR: register_process: proclib folder not found, check install_path or install libraries.
~~~
In order to fix this, you have to re-copy the libraries, see the end of `setup.sh` for the recipe.

## Step0: environment

We use rootpy in the plotting code, which is installed on the T3 locally in `~jpata/anaconda2`. In order to properly configure the environment, run the following `source setenv_psi.sh` before starting your work.

## Step1: VHBB code
This will start with MiniAOD and produce a VHBB ntuple.

In order to run a quick test of the code, use the following makefile
~~~
$ cd $CMSSW_BASE/src/VHbbAnalysis/Heppy/test
$ python validation/tth_sl_dl.py #run a few MC files
$ python validation/tth_data.py #run a few data files
~~~

The structure of the VHBB-tree is encoded in `$CMSSW_BASE/src/TTH/MEAnalysis/python/VHbbTree.py` for MC and `VHbbTreeData.py` for data. These files are **automatically generated** using `make vhbb_wrapper` with the following commands:

~~~
cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test && python genWrapper.py
cd $(CMSSW_BASE)/src/VHbbAnalysis/Heppy/test && python genWrapper_data.py
~~~

Submitting jobs based on step1 will proceed via `crab3`, explained in Step1+2.

## Step2: tthbb code
Using the VHBB-tree, we will run the ttH(bb) and matrix element code (tthbb13)

In order to test the code, run:
~~~
$ python $CMSSW_BASE/src/TTH/MEAnalysis/python/test_MEAnalysis_heppy.py
~~~

This will call
~~~
python $CMSSW_BASE/src/TTH/MEAnalysis/python/MEAnalysis_heppy.py
~~~
which is currently configured by the `MEAnalysis_cfg_heppy.py` master configuration.

## Step1+2: VHBB & tthbb13 with CRAB
In order to reduce the amount of intermediate steps and book-keeping, we run step1 (VHBB) and step2 (tthbb13) together in one job, back to back. This is configured in `$CMSSW_BASE/src/TTH/MEAnalysis/crab_vhbb

To submit a few test workflows with crab do:

~~~
$ cd TTH/MEAnalysis/crab_vhbb
$ python multicrab.py --workflow testing_withme --tag my_test1
~~~

To produce all the SL/DL samples, do
~~~
$ cd TTH/MEAnalysis/crab_vhbb
$ python multicrab.py --workflow leptonic --tag May13
~~~
where the tag `May13` is for your own book-keeping.

To prepare the dataset files in `TTH/MEAnalysis/gc/datasets/{TAG}/{DATASET}`, use the DAS script
~~~
$ python TTH/MEAnalysis/python/MakeDatasetFiles.py --version {TAG}
~~~

This will create lists of the Step1+2 files in the Storage Element (SE), which are stored under `TTH/MEAnalysis/gc/datasets/{TAG}`.

## Step3: skim with `projectSkim`

When some of the samples are done, you can produce smallish (<10GB) skims of the files using local batch jobs.

~~~
$ cd TTH/MEAnalysis/gc
$ source makeEnv.sh #make an uncommited script to properly set the environment on the batch system
v./grid-control/go.py confs/projectSkim.conf
... #wait
$ ./hadd.py /path/to/output/GC1234/ #call our merge script
~~~

This will produce some skimmed ntuples in
~~~
/mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GCe0f041d65b98:
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8 <= unmerged
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8.root <= merged file
...
Jul15_leptonic_v1__TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
Jul15_leptonic_v1__TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
Jul15_leptonic_v1__TTTo2L2Nu_13TeV-powheg.root
Jul15_leptonic_v1__TT_TuneCUETP8M1_13TeV-powheg-pythia8.root
~~~

The total processed yields (ngen) can be extracted with
~~~
$ cd TTH/MEAnalysis/gc
$ ./grid-control/go.py confs/count.conf
...
$ ./hadd.py /path/to/output/GC1234/
$ python $CMSSW_BASE/src/TTH/MEAnalysis/python/getCounts.py /path/to/output/GC1234/
~~~

The counts need to be introduced to `TTH/Plotting/python/Datacards/config_*.cfg` as the `ngen` flags for the samples.

## Step4: N-dimensional histograms with `Plotting/python/joosep/sparsinator.py`
In order to industrially produce all variated histograms, we create an intermediate file containing ROOT `THnSparse` histograms of the samples with appropriate systematics.

~~~
$ cd TTH/MEAnalysis/gc
$ ./grid-control/go.py confs/sparse.conf
...
$ hadd -f sparse.root /path/to/output/GC1234/
~~~

The output file will contain
~~~
$ 
TTTo2L2Nu_13TeV-powheg <- sample
-dl <- base category ({sl,dl,fh})
--sparse (THnSparseT<TArrayF>) <==== nominal distribution
--sparse_CMS_ttH_CSVHFDown (THnSparseT<TArrayF>) <==== systematically variated distributions
--sparse_CMS_ttH_CSVHFStats1Down (THnSparseT<TArrayF>)
--sparse_CMS_ttH_CSVHFStats1Up (THnSparseT<TArrayF>)
--sparse_CMS_ttH_CSVHFStats2Down (THnSparseT<TArrayF>)
--sparse_CMS_ttH_CSVHFStats2Up (THnSparseT<TArrayF>)
--sparse_CMS_ttH_CSVHFUp (THnSparseT<TArrayF>)
-sl
...
ttHTobb_M125_13TeV_powheg_pythia8
-dl
...
-sl
...
...
~~~

## Step5: Categories with `makecategories.sh`

Configure what is necessary in `TTH/Plotting/python/Datacards/config_*.cfg`, then call

~~~
cd TTH/MEAnalysis/gc
#generate the parameter csv files: analysis_groups.csv, analysis_specs.csv
python $CMSSW_BASE/src/TTH/Plotting/python/Datacards/AnalysisSpecification.py
./grid-control/go.py confs/makecategories.conf
~~~

This will create all the `combine` datacards (`{ANALYSIS}/{CATEGORY}.root` files and `shapes_*.txt` files) for all analyses and all the categories.

~~~
[jpata@t3ui17 gc]$ ls -1 ~/tth/gc/makecategory/GC41c32de9adb2/SL_7cat/
shapes_sl_j4_t3_blrH_mem_SL_0w2h2t_p.txt
shapes_sl_j4_t3_blrL_btag_LR_4b_2b_btagCSV_logit.txt
shapes_sl_j4_t3_mem_SL_0w2h2t_p.txt
shapes_sl_j4_tge4_mem_SL_0w2h2t_p.txt
shapes_sl_j5_t3_blrH_mem_SL_1w2h2t_p.txt
shapes_sl_j5_t3_blrL_btag_LR_4b_2b_btagCSV_logit.txt
shapes_sl_j5_t3_mem_SL_1w2h2t_p.txt
shapes_sl_j5_tge4_mem_SL_1w2h2t_p.txt
shapes_sl_jge6_t2_btag_LR_4b_2b_btagCSV_logit.txt
shapes_sl_jge6_t3_blrH_mem_SL_2w2h2t_p.txt
shapes_sl_jge6_t3_blrL_mem_SL_2w2h2t_p.txt
shapes_sl_jge6_t3_mem_SL_2w2h2t_p.txt
shapes_sl_jge6_tge4_mem_SL_2w2h2t_p.txt
sl_j4_t3_blrH.root
sl_j4_t3_blrL.root
sl_j4_t3.root
sl_j4_tge4.root
sl_j5_t3_blrH.root
sl_j5_t3_blrL.root
sl_j5_t3.root
sl_j5_tge4.root
sl_jge6_t2.root
sl_jge6_t3_blrH.root
sl_jge6_t3_blrL.root
sl_jge6_t3.root
sl_jge6_tge4.root

$ python ../test/listroot.py ~/tth/gc/makecategory/GC41c32de9adb2/SL_7cat/sl_jge6_tge4.root
ttH_hbb
-sl_jge6_tge4
--btag_LR_4b_2b_btagCSV_logit (Hist)
--jetsByPt_0_pt (Hist)
--mem_SL_2w2h2t_p (Hist)
ttbarPlusB
-sl_jge6_tge4
--btag_LR_4b_2b_btagCSV_logit (Hist)
--jetsByPt_0_pt (Hist)
--mem_SL_2w2h2t_p (Hist)
...
~~~

## Step6: Limits with `makelimits.sh`

Configure the path to the category output in `confs/makelimits.conf` by setting `datacardbase` to the output of step 4.

~~~
cd TTH/MEAnalysis/gc
./grid-control/go.py confs/makelimits.conf
~~~

## Step6: data/mc plots

From the output of makecategory, you can make data/MC plots using code in `plotlib.py` and `controlPlot.py`. See `TTH/MEAnalysis/python/joosep/controlPlot.py` for an example. For this to work, you need to use the rootpy environment.

On the T3 using 10 cores, you can make about 100 pdf plots per minute.

## Step3-6 in one go: `launcher.py`

There is a new workflow in order to run all the post-ntuplization steps in one workflow. It relies on a central "job broker" and a launcher script.
**Important**: only one broker can run per T3 UI!

Start the job broker (redis database) by going to
~~~
cd TTH/MEAnalysis/rq/
source env.sh
./server.sh
~~~

Then in another screen, launch jobs that will connect to the broker and wait for instructions
~~~
cd TTH/MEAnalysis/rq/
source env.sh
./sub.sh
~~~

Then launch the actual workflow
~~~
source env.sh
python launcher.py TTH/Plotting/python/Datacards/config_*.cfg
~~~

You will see the progress of various steps, the results will end up in `TTH/MEAnalysis/rq/results`.

When you're done, don't forget to free up your jobs:
~~~
qdel -u $USER
~~~

=================================================================================================================
Old README
=================================================================================================================

# TTHBB MEM code

Setup on SLC6 in a clean directory (no CMSSW) on a **shared file system**
~~~
mkdir -p ~/tth/sw
cd ~/tth/sw
wget --no-check-certificate https://raw.githubusercontent.com/silviodonato/tthbb13/ttH80X/setup.sh
source setup.sh
~~~
This will download CMSSW, the tthbb code and all the dependencies.

In order to compile the code, run
~~~
cd ~/tth/sw/CMSSW/src
cmsenv
scram b -j 8
~~~

## Step0: environment

We use rootpy in the code, which is installed on the T3 locally in `~jpata/rootpy`. In order to properly configure the environment, run the following `source setenv_psi.sh` and `source setenv_sklearn_cmssw.sh`before starting your work.

## Step1: VHBB code
This will start with MiniAOD and produce a VHBB ntuple.

In order to run a quick test of the code, use the following makefile
~~~
cd $CMSSW_BASE/src/TTH
#edit nEvents in  $CMSSW_BASE/src/VHbbAnalysis/Heppy/test/vhbb_combined.py 
#edit files in  $CMSSW_BASE/src/VHbbAnalysis/Heppy/test/vhbb.py (eg. /store/mc/RunIISpring16MiniAODv2/ttHJetTobb_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext3-v2/70000/001C3ACD-2C31-E611-A7EE-003048F5ADF6.root or  root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv2/ttHTobb_M125_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40000/0089CC67-6338-E611-947D-0025904C4E2A.root)
make test_VHBB >& logTestVHbb &
#this will call VHbbAnalysis/Heppy/test/vhbb_combined.py
~~~

Submission will proceed via `crab3`, explained in Step1+2.

## Step2: tthbb code
Using the VHBB ntuple, we will run the ttH(bb) and matrix element code

This is to test the code
~~~
cd $CMSSW_BASE/src/TTH/tests_out
python moveTTree.py #simple script that moves VHBB.root in new.root and 'tree' in 'vhbb/tree'
cd $CMSSW_BASE/src/TTH
#edit testfile_vhbb_tthbb in $CMSSW_BASE/src/TTH/Makefile
#eg. file:///scratch/sdonato/ttH/test/CMSSW/src/TTH/tests_out/new.root
make test_MEAnalysis >& logTestME &
#this will call TTH/MEAnalysis/python/MEAnalysis_heppy.py
~~~

## Step1+2: VHBB & tthbb13 with CRAB

To submit a few test workflows with crab do:

~~~
cd $CMSSW_BASE/src/TTH/MEAnalysis/crab_vhbb
## remove possible missing datasets in multicrab.py
python multicrab.py --workflow testing_withme --tag my_test1
~~~

To produce all the hadronic samples, do
~~~
cd TTH/MEAnalysis/crab_vhbb
python multicrab.py --workflow hadronic --tag had_V23
~~~

To prepare the dataset files in `TTH/MEAnalysis/gc/datasets/{TAG}/{DATASET}`, use the DAS script
~~~
cd $CMSSW_BASE/src/TTH/MEAnalysis/gc/datasets
#produce the dataset folder
/afs/cern.ch/user/v/valya/public/das_client.py --limit 0 --query "dataset dataset=/*/sdonato-data_Aug15-*/USER instance=prod/phys03"  > datasetsFH.txt
#check and remove duplicates in datasetsFH.txt
cd $CMSSW_BASE/src/TTH/MEAnalysis/gc/
python ../python/MakeDatasetFiles.py --datasetfile datasets/datasetsFH.txt --version had_V24_2 --instance prod/phys03
~~~

## Step3: skim with `projectSkim`

When some of the samples are done, you can produce smallis (<10GB) skims of the files using local batch jobs.

~~~
cd $CMSSW_BASE/src/TTH/MEAnalysis/python
#edit prepareSamples.py
python prepareSamples.py
scram b
cd $CMSSW_BASE/src/TTH/MEAnalysis/gc
source makeEnv.sh
#edit confs/projectSkimFH.conf
#eg. find datasets/had_V24/ | grep tth
#edit confs/projectSkimDataFH.conf

./grid-control/go.py confs/projectSkimFH.conf -cG
./grid-control/go.py confs/projectSkimDataFH.conf -cG
...
./hadd.py ~/tth/gc/projectSkimFH/GCb7f111222333/ #for mc
./hadd.py ~/tth/gc/projectSkimDataFH/GCb7f111222334/ #for data
~~~

This will produce some skimmed ntuples in
~~~
/mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GCe0f041d65b98:
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8 <= unmerged
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8.root <= merged file
Jul15_leptonic_v1__TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
...
~~~

The total processed yields can be extracted with
~~~
cd $CMSSW_BASE/src/TTH/MEAnalysis/gc
#edit confs/countFH.conf 
./grid-control/go.py confs/countFH.conf -cG
...
./hadd.py ~/tth/gc/count/GC1234/
python $CMSSW_BASE/src/TTH/MEAnalysis/python/getCounts.py `ls ~/tth/gc/count/GC1234/*.root`
~~~

The counts need to be introduced to `$CMSSW_BASE/src/TTH/MEAnalysis/python/inputs.py` as the `ngen` dictionary.

Step3: N-dimensional histograms with `Plotting/python/joosep/sparsinator.py`
------------------
In order to industrially produce all variated histograms, we create an intermediate file containing ROOT THnSparse histograms of the samples with appropriate systematics.

First test the `sparsinator.py` locally:
~~~
source $CMSSW_BASE/src/TTH/setenv_psi.sh
source $CMSSW_BASE/src/TTH/setenv_sklearn_cmssw.sh
cd $CMSSW_BASE/src/TTH
#edit datasets, files, and histo folder in Plotting/python/test_sparsinator.py
python Plotting/python/test_sparsinator.py
~~~
then, launch the sparsinator:
~~~
cd $CMSSW_BASE/src/TTH/MEAnalysis/gc
#edit confs/sparseFH.conf
./grid-control/go.py confs/sparseFH.conf -cG
~~~

The output file will contain
~~~
$ 
TTTo2L2Nu_13TeV-powheg <- sample
-dl <- base category ({sl,dl,fh})
--sparse (THnSparseT<TArrayF>) <==== nominal distribution
--sparse_CMS_ttH_CSVHFDown (THnSparseT<TArrayF>) <==== systematically variated distributions
--sparse_CMS_ttH_CSVHFStats1Down (THnSparseT<TArrayF>)
-sl
...
ttHTobb_M125_13TeV_powheg_pythia8
-dl
...
-sl
...
...
~~~

Once the jobs are done:
~~~
hadd ControlPlotsSparse.root `find ~/tth/gc/sparseFH/GCde1112222333 -name "*.root"`
~~~
This creates a histogram file `ControlPlotsSparse.root`


Step4: Categories with `makecategories.sh`
-----------------

Configure the input file in `TTH/Plotting/python/Datacards/config_fh.cfg`, then call

~~~
cd $CMSSW_BASE/src/TTH/MEAnalysis/gc
#generate the parameter csv files: analysis_groups.csv, analysis_specs.csv
#edit $CMSSW_BASE/src/TTH/Plotting/python/Datacards/config_fh.cfg (at least "sparse_version")
#edit $CMSSW_BASE/src/TTH/Plotting/python/Datacards/AnalysisSpecification.py (use only analyses_FH)
python $CMSSW_BASE/src/TTH/Plotting/python/Datacards/AnalysisSpecification.py

#edit and test make-category 
python ../../Plotting/python/test_MakeCategory.py

#edit confs/makecategory.conf (change at least "workdir")
./grid-control/go.py confs/makecategory.conf -cG
~~~

This will create all the `combine` datacards (`{ANALYSIS}/{CATEGORY}.root` files and `shapes_*.txt` files) for all analyses and all the categories.

~~~
[jpata@t3ui17 gc]$ ls -1 ~/tth/gc/makecategory/GC41c32de9adb2/SL_7cat/
shapes_sl_j4_t3_blrH_mem_SL_0w2h2t_p.txt
shapes_sl_j4_t3_blrL_btag_LR_4b_2b_btagCSV_logit.txt
shapes_sl_j4_t3_mem_SL_0w2h2t_p.txt
shapes_sl_j4_tge4_mem_SL_0w2h2t_p.txt
shapes_sl_j5_t3_blrH_mem_SL_1w2h2t_p.txt
shapes_sl_j5_t3_blrL_btag_LR_4b_2b_btagCSV_logit.txt
shapes_sl_j5_t3_mem_SL_1w2h2t_p.txt
shapes_sl_j5_tge4_mem_SL_1w2h2t_p.txt
shapes_sl_jge6_t2_btag_LR_4b_2b_btagCSV_logit.txt
shapes_sl_jge6_t3_blrH_mem_SL_2w2h2t_p.txt
shapes_sl_jge6_t3_blrL_mem_SL_2w2h2t_p.txt
shapes_sl_jge6_t3_mem_SL_2w2h2t_p.txt
shapes_sl_jge6_tge4_mem_SL_2w2h2t_p.txt
sl_j4_t3_blrH.root
sl_j4_t3_blrL.root
sl_j4_t3.root
sl_j4_tge4.root
sl_j5_t3_blrH.root
sl_j5_t3_blrL.root
sl_j5_t3.root
sl_j5_tge4.root
sl_jge6_t2.root
sl_jge6_t3_blrH.root
sl_jge6_t3_blrL.root
sl_jge6_t3.root
sl_jge6_tge4.root

$ python ../test/listroot.py ~/tth/gc/makecategory/GC41c32de9adb2/SL_7cat/sl_jge6_tge4.root
ttH_hbb
-sl_jge6_tge4
--btag_LR_4b_2b_btagCSV_logit (Hist)
--jetsByPt_0_pt (Hist)
--mem_SL_2w2h2t_p (Hist)
ttbarPlusB
-sl_jge6_tge4
--btag_LR_4b_2b_btagCSV_logit (Hist)
--jetsByPt_0_pt (Hist)
--mem_SL_2w2h2t_p (Hist)
...
~~~

## Step5: Limits with `makelimits.sh`

Configure the path to the category output in `confs/makelimits.conf` by setting `datacardbase` to the output of step 4.

~~~
cd $CMSSW_BASE/src/TTH/MEAnalysis/gc
cp local-example.conf local.conf 
## edit confs/makelimits.conf to change datacardbase (eg. /mnt/t3nfs01/data01/shome/sdonato/tth/gc/makecategory/GC46066f85f573/)
vi confs/makelimits.conf
./grid-control/go.py confs/makelimits.conf
~~~

## Step6: data/mc plots

From the output of makecategory, you can make data/MC plots using code in `plotlib.py` and `controlPlot.py`. See `$CMSSW_BASE/src/TTH/Plotting/python/joosep/controlPlot.py` for an example. For this to work, you need to use the rootpy environment.
~~~
cd $CMSSW_BASE/src/TTH/Plotting/python/joosep

eval `scramv1 runtime -sh`
export PYTHONPATH=/mnt/t3nfs01/data01/shome/jpata/anaconda/lib/python2.7/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/shome/jpata/anaconda/lib/:$LD_LIBRARY_PATH
export PATH=/mnt/t3nfs01/data01/shome/jpata/anaconda/bin:$PATH
##or try /mnt/t3nfs01/data01/shome/sdonato/anaconda2
# just after ssh
# eval `scramv1 runtime -sh`
# export PYTHONPATH=/mnt/t3nfs01/data01/shome/jpata/anaconda/lib/python2.7/site-packages:$PYTHONPATH
# export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/shome/sdonato/anaconda2/lib/:$LD_LIBRARY_PATH
# export PATH=/mnt/t3nfs01/data01/shome/sdonato/anaconda2/bin:$PATH


#check the variables saved in your categories
python $CMSSW_BASE/src/TTH/MEAnalysis/test/listroot.py ~/tth/gc/makecategory/GC1111222223333/FH/fh_j9_t4.root
#edit controlPlot.py (add and use only "cats_fh"; change args; change get_base_plot to eg. /shome/sdonato/tth/gc/makecategory/GCdedfe5320b02/; check which variable you want to plot; disable systematics if you want)
python controlPlot.py
#possibly, fix missing variables in plotlib.py
~~~

On the T3 using 10 cores, you can make about 100 pdf plots per minute.


## Other: files to be changed to run the fully hadronic tth

TTH/MEAnalysis/python/samples_base.py:
  - PROCESS_MAP
  - TRIGGER_MAP

TTH/Plotting/python/joosep/sparsinator.py:
  - add Var(name="is_fh")
  - add Var(name="mem_FH_4w2h2t_p", ....
  - (?) add Var(name="HLT_ttH_FH",...
  - add Axis("mem_FH_4w2h2t_p",...
  - add 'fh' section in createOutputs
  - add definition of pass_HLT_fh(event):
  - add 'fh' case in triggerPath
  - add: dirs["fh"] = dirs["sample"].mkdir("fh")
  - add "or event.is_fh" after "apply some basic preselection"


TTH/Plotting/python/Datacards/AnalysisSpecificationSL.py:
  - in _lumis, add "fh": lumi["BTagCSV"]"
  - add "BTagCSV" as DataSample -> triggerPath cut!
  - 

TTH/Plotting/python/Datacards/AnalysisSpecificationFH.py:
  - everything

TTH/Plotting/python/Datacards/AnalysisSpecification.py:
  - add FH
  - (?) do not loop over SL and DL

TTH/Plotting/python/joosep/plotlib.py:
  - add mem_FH_* variables
  - add QCD in colors
  - check cats
  - add QCD in samplelist

TTH/Plotting/python/joosep/controlPlot.py:
  - add QCD in procs_names
  - add "cats_fh"
  - run on cats_fh instead of SL and DL

## Debug: VHbb+ttH ntuplizer test

You can test the VHbb+ttH ntuplizer before the CRAB submission using:
~~~
cd $CMSSW_BASE/src/TTH/MEAnalysis/crab_vhbb
source $CMSSW_BASE/src/TTH/setenv_psi.sh
source $CMSSW_BASE/src/TTH/setenv_sklearn_cmssw.sh
rm -r Output* #otherwise it will crash (at the end it looks for "Output/tree.root")
#edit heppy_crab_script.py: use PSet.py instead of PSet_local.py
FILE_NAMES="file:///shome/sdonato/QCD_HT2000toInf_MINIAODSIM.root" MAX_EVENTS=100 SKIP_EVENTS=0 python --local heppy_crab_script.py >& log &
#restore heppy_crab_script.py: use PSet_local.py instead of PSet.py

~~~
