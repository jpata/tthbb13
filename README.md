TTHBB MEM code
==============

Setup on SLC6 in a clean directory (no CMSSW)
~~~
mkdir -p ~/tth/sw
cd ~/tth/sw
wget --no-check-certificate https://raw.githubusercontent.com/jpata/tthbb13/master/setup.sh
source setup.sh
~~~
This will download CMSSW, the tthbb code and all the dependencies.



Step1: VHBB code
----------------
~~~
make test_VHBB
~~~

Step2: tthbb code
--------------------
Running the MEM code

~~~
make test_MEAnalysis
~~~

This will execute
~~~
python TTH/MEAnalysis/python/MEAnalysis_heppy.py
~~~
