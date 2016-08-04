# Use version from IB until it migrates to the main release
# Should work as long as both releases have same python version
# Will need to update this path once in a while
export IB_BASE=/cvmfs/cms-ib.cern.ch/2016-32/slc6_amd64_gcc530
export PYTHONPATH=$IB_BASE/external/py2-numpy/1.11.1/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-scikit-learn/0.17.1/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-pandas/0.17.1-agcabg/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-matplotlib/1.5.2/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-scipy/0.16.1/lib/python2.7/site-packages:$PYTHONPATH
#export PYTHONPATH=$IB_BASE/lcg/root/6.06.04-agcabg/lib:$PYTHONPATH