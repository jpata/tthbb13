tthbb13 setup
=======

1. Create the working directory ``mkdir my_tth;cd my_tth``
2. Create the CMSSW directory by executing the commands in ``setup.sh`` "manually" (you can download the file and source it)
3. Get the TTH code into the CMSSW directory ``cd CMSSW/src/TTH;git clone https://github.com/jpata/tthbb13.git``
4. Compile ``scram b``
5. Run the TTH tests ``cd CMSSW/src/TTH;scram b runtests``


To test manually, you can study *TTH/MakeFile* and run
~~~
  make -F my_tth/CMSSW/src/TTH/Makefile debug
  make -F my_tth/CMSSW/src/TTH/Makefile run_debug
~~~

A sample file should be produced at ``my_tth/ntuple.root``.

To configure the environment (in a custom batch job), call
~~~
  source my_tth/setenv.sh
~~~


Code overview
=============

The analysis steps are as follows

1. The step *TTH/TTHNtupleAnalyzer* prepares a simple flat analysis ntuple from miniAOD. The TTree format is specified by the file ``TTH/TTHNtupleAnalyzer/interface/tth_tree.hh``. This is run using CRAB3.
2. *TTH/MEAnalysis* calculates the matrix-element related analysis code, operating on the output of *TTH/TTHNtupleAnalyzer*
