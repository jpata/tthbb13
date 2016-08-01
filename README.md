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

## Step0: environment

We use rootpy in the code, which is installed on the T3 locally in `~jpata/rootpy`. In order to properly configure the environment, run the following `source setenv_psi.sh` before starting your work.

## Step1: VHBB code
This will start with MiniAOD and produce a VHBB ntuple.

In order to run a quick test of the code, use the following makefile
~~~
$ make test_VHBB
# this will call VHbbAnalysis/Heppy/test/vhbb_combined.py
$ make test_VHBB_data
# this will call VHbbAnalysis/Heppy/test/vhbb_combined_data.py
~~~

Submission will proceed via `crab3`, explained in Step1+2.

## Step2: tthbb code
Using the VHBB ntuple, we will run the ttH(bb) and matrix element code

This is to test the code
~~~
$ make test_MEAnalysis
#this will call TTH/MEAnalysis/python/MEAnalysis_heppy.py
$ make test_MEAnalysis_withme
#this will call TTH/MEAnalysis/python/MEAnalysis_heppy.py
~~~

## Step1+2: VHBB & tthbb13 with CRAB

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

To prepare the dataset files in `TTH/MEAnalysis/gc/datasets/{TAG}/{DATASET}`, use the DAS script
~~~
$ python TTH/MEAnalysis/python/MakeDatasetFiles.py --version {TAG}
~~~

## Step3: skim with `projectSkim`

When some of the samples are done, you can produce smallis (<10GB) skims of the files using local batch jobs.

~~~
$ cd TTH/MEAnalysis/gc
$ source makeEnv.sh #make an uncommited script to properly set the environment on the batch system
v./grid-control/go.py confs/projectSkim.conf
... #wait
$ ./hadd.py /path/to/output/GC1234/
~~~

This will produce some skimmed ntuples in
~~~
/mnt/t3nfs01/data01/shome/jpata/tth/gc/projectSkim/GCe0f041d65b98:
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8 <= unmerged
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8.root <= merged file
Jul15_leptonic_v1__TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
Jul15_leptonic_v1__TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
Jul15_leptonic_v1__TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
Jul15_leptonic_v1__TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root
Jul15_leptonic_v1__TTTo2L2Nu_13TeV-powheg
Jul15_leptonic_v1__TTTo2L2Nu_13TeV-powheg.root
Jul15_leptonic_v1__TT_TuneCUETP8M1_13TeV-powheg-pythia8
Jul15_leptonic_v1__TT_TuneCUETP8M1_13TeV-powheg-pythia8.root
~~~

The total processed yields can be extracted with
~~~
$ cd TTH/MEAnalysis/gc
$ ./grid-control/go.py confs/count.conf
...
$ ./hadd.py /path/to/output/GC1234/
$ python $CMSSW_BASE/src/TTH/MEAnalysis/python/getCounts.py /path/to/output/GC1234/
~~~

The counts need to be introduced to `TTH/MEAnalysis/python/samples_base.py` as the `ngen` dictionary.

Step3: N-dimensional histograms with `Plotting/python/joosep/sparsinator.py`
------------------
In order to industrially produce all variated histograms, we create an intermediate file containing ROOT THnSparse histograms of the samples with appropriate systematics.

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

Step4: Categories with `makecategories.sh`
-----------------

Configure the input file in `TTH/Plotting/python/Datacards/AnalysisSpecificationSL.py`, then call

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

## Step5: Limits with `makelimits.sh`

Configure the path to the category output in `confs/makelimits.conf` by setting `datacardbase` to the output of step 4.

~~~
cd TTH/MEAnalysis/gc
./grid-control/go.py confs/makelimits.conf
~~~

## Step6: data/mc plots

From the output of makecategory, you can make data/MC plots using code in `plotlib.py` and `controlPlot.py`.

See `TTH/MEAnalysis/python/joosep/controlPlot.py` for an example.

For this to work, you need to use the rootpy environment.
