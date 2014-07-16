tthbb13
=======

1. ``mkdir my_tth;cd my_tth``
2. execute the commands in ``setup.sh`` "manually"
3. ``cd CMSSW/src/TTH;git clone https://github.com/jpata/tthbb13.git``
4. ``scram b``


To test, run
~~~
  make -F my_tth/CMSSW/src/TTH/Makefile debug
  make -F my_tth/CMSSW/src/TTH/Makefile run_debug
~~~

A sample file should be produced at ``my_tth/ntuple.root``.



To configure the environment (in a batch job), run
~~~
  source my_tth/setenv.sh
~~~
