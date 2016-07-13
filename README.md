TTHBB MEM code
==============

Setup on SLC6 in a clean directory (no CMSSW)
~~~
mkdir -p ~/tth/sw
cd ~/tth/sw
wget --no-check-certificate https://raw.githubusercontent.com/jpata/tthbb13/meanalysis-80x/setup.sh
source setup.sh
~~~
This will download CMSSW, the tthbb code and all the dependencies.



Step1: VHBB code
----------------
This will start with MiniAOD and produce a VHBB ntuple.

~~~
make test_VHBB
#this will call VHbbAnalysis/Heppy/test/vhbb_combined.py
~~~

Step2: tthbb code
--------------------
Using the VHBB ntuple, we will run the ttH(bb) and matrix element code

~~~
make test_MEAnalysis
#this will call TTH/MEAnalysis/python/MEAnalysis_heppy.py
~~~

Step1+2: VHBB & tthbb13 with CRAB
---------------------------------

To submit a few test workflows with crab do:

~~~
cd TTH/MEAnalysis/crab_vhbb
python multicrab.py --workflow testing_withme --tag my_test1
~~~

To produce all the SL/DL samples, do
~~~
cd TTH/MEAnalysis/crab_vhbb
python multicrab.py --workflow leptonic --tag May13
~~~


Step3: skim with `projectSkim.sh`
------------------
When some of the samples are done, you can produce small (<5GB) skims of the files using

~~~
cd TTH/MEAnalysis/gc
./grid-control/go.py confs/projectSkim.conf
...
./hadd.py /path/to/output/GC1234/
~~~

The total processed yields can be extracted with
~~~
cd TTH/MEAnalysis/gc
./grid-control/go.py confs/count.conf
...
./hadd.py /path/to/output/GC1234/
python ../python/getCounts.py /path/to/output/GC1234/
~~~

Step3: Sparse histograms with `Plotting/bin/MELooper.cc`
------------------
In order to industrially produce all variated histograms, we create an intermediate file containing ROOT THnSparse histograms of the samples.

First make the `melooper` exe:
~~~
cd TTH
make melooper
~~~

Then submit the jobs
~~~
cd TTH/MEAnalysis/gc
./grid-control/go.py confs/plots.conf
~~~

Once the jobs are done:
~~~
hadd ControlPlotsSparse.root `find /path/to/output/GC1234/ -name "*.root"`
~~~
This creates a histogram file `ControlPlotsSparse.root`

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
