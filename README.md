Top Tagging Ntuple Making (based on TTH-MEM Ntuple)
==============

Setup on SLC6
~~~
mkdir TTH
cd TTH
wget --no-check-certificate https://raw.githubusercontent.com/jpata/tthbb13/dev-73X/setup.sh
source setup.sh
~~~

As the default Ntuple is for TTH we need to change a few branches:
~~~
cd TTHNtupleAnalyzer/python
python headergen.py ../interface/tth_tree_template.hh ../interface/tth_tree.hh tagger_branches.py
~~~

Now everything is ready for compilation:
~~~
cd $CMSSW_BASE/src
scram b -j 10
~~~

To test the Ntuple making:
(first download a MiniAOD (CSA14 and Phys14 should both do, Pythia6 will have problems with parton matching) and set the path to it in taggers_cfg)
~~~
cd TTH/TTHNtupleAnalyzer/test
cmsRun taggers_cfg.py
~~~

"Step 2" (per top/parton) Ntuples can be created with the script:
~~~
TTH/TTHNtupleAnalyzer/python/MakeTaggingNtuple.py
~~~

Some plotting examples are in:
~~~~
TTH/Plotting/python/gregor
~~~

TODO:
==============
*  "Step 2" Ntuples production on Grid
*  Cleanup of Plotting code
*  Simplify configurations
*  Add b-tagging, ECF, SD


