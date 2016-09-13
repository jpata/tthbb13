# the packages are now in the right scram_arch but we need to select the right versions
export OVERRIDE_PATH_BASE=/cvmfs/cms.cern.ch/$SCRAM_ARCH/external
export PYTHONPATH=$OVERRIDE_PATH_BASE/py2-numpy/1.11.1/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$OVERRIDE_PATH_BASE/py2-pandas/0.17.1-agcabg/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$OVERRIDE_PATH_BASE/py2-matplotlib/1.5.2/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$OVERRIDE_PATH_BASE/py2-scipy/0.16.1/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$OVERRIDE_PATH_BASE/py2-scikit-learn/0.17.1/lib/python2.7/site-packages:$PYTHONPATH
