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

## Step1: VHBB code
This will start with MiniAOD and produce a VHBB ntuple.

In order to run a quick test of the code, use the following makefile
~~~
$ make test_VHBB
#this will call VHbbAnalysis/Heppy/test/vhbb_combined.py
$ make test_VHBB
#this will call VHbbAnalysis/Heppy/test/vhbb_combined.py
~~~

Submission will proceed via `crab3`, explained later.

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

When some of the samples are done, you can produce small (<5GB) skims of the files using local batch jobs.

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
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8
Jul15_leptonic_v1__ttHTobb_M125_13TeV_powheg_pythia8.root
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

Step5: Limits with `makelimits.sh`
-----------------

Configure the path to the category output in `confs/makelimits.conf` by setting `datacardbase` to the output of step 4.

~~~
cd TTH/MEAnalysis/gc
./grid-control/go.py confs/makelimits.conf
~~~
