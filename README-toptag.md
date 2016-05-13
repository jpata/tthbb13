Top Tagging Ntuple Making (based on TTH-MEM Ntuple)
==============

### Setup on SLC6
~~~
mkdir TTH
cd TTH
wget --no-check-certificate https://raw.githubusercontent.com/jpata/tthbb13/dev-73X/setup.sh
source setup.sh
~~~

When running later just execute
~~~
export SCRAM_ARCH=slc6_amd64_gcc491
~~~
before setting up the CMS environment.

Now everything is ready for compilation:
~~~
cd $CMSSW_BASE/src
scram b -j 10
~~~

As the default Ntuple is for TTH we need to change a few branches:
~~~
cd TTH/TTHNtupleAnalyzer/python
python headergen.py ../interface/tth_tree_template.hh ../interface/tth_tree.hh tagger_branches.py
~~~

Re-Compile the TTHNtupleAnalyzer:
~~~
cd $CMSSW_BASE/src/TTH/TTHNtupleAnalyzer
scram b -j 10
~~~




### NTuple Production


To test the Ntuple making:
(first download a MiniAOD (CSA14 and Phys14 should both do, Pythia6 will have problems with parton matching) and set the path to it in taggers_cfg)
~~~
cd TTH/TTHNtupleAnalyzer/test
cmsRun taggers_cfg.py
~~~

"Step 2" (per top/parton) Ntuples can be created with the script:
(this is now automatically run on the grid if you submit via crab_ntuples/ntop.py - see below)
~~~
TTH/TTHNtupleAnalyzer/python/MakeTaggingNtuple.py
~~~

You should also either comment out Shower Deconstruction or ping Gregor to get added to the private github repo that contains the code.

### Adding Variables

New grooming settings can be added by modifying:
~~~
TTH/TTHNtupleAnalyzer/python/Taggers_cfg.py
~~~

These changes should be automatically picked up py

~~~
TTH/TTHNtupleAnalyzer/python/tagger_branches.py
TTH/TTHNtupleAnalyzer/python/MakeTaggingNtuple.py
~~~

Do not forget to re-run the headergen step and recompile after changing the grooming settings.


### Grid Submission:
The grid submission scripts are in: 
~~~
TTH/TTHNtupleAnalyzer/crab_configs
~~~

The submission is done by ntop.py which relies on ~~~../python/CrabHelpers.py~~~ Most of the parameters are set in c_TEMPLATE.py and the actual thing that runs on the grid is myScript.sh

### Plotting

Some plotting examples are in:
~~~
TTH/Plotting/python/gregor
~~~

First you will want to run something similar to:
~~~
Plotting/python/gregor/GetPtWeight.py
~~~

This will produce a file storing the re-weighting functions for pT and eta. Then run
~~~
TTHNtupleAnalyzer/python/AddWeights.py
~~~
to make a new file with the weights included (it also adds a pt and eta branch that copy either the hadronic top or the qcd parton).

Everything else comes afterwards.
Most of the control plots are in
~~~
CheckPtWeight.py
~~~
Examples for MutualInformation:
~~~
TestMutualInformation.py
~~~
Examples for TMVA:
~~~
ClassifyTaggers.py
~~~

I've started centralizing the per-Sample information in TopSamples.pyand the per-Variable information in TopTaggingVariables.py.




