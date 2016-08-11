eval `scramv1 runtime -sh`
#export PYTHONPATH=/mnt/t3nfs01/data01/shome/jpata/anaconda/lib/python2.7/site-packages:$PYTHONPATH
#export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/shome/jpata/anaconda/lib/:$LD_LIBRARY_PATH
#export PATH=/mnt/t3nfs01/data01/shome/jpata/anaconda/bin:$PATH
export IB_BASE=/cvmfs/cms-ib.cern.ch/week0/slc6_amd64_gcc530
export PYTHONPATH=$IB_BASE/external/py2-numpy/1.11.1/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-scikit-learn/0.17.1/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-pandas/0.17.1-agcabg/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-matplotlib/1.5.2/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-scipy/0.16.1/lib/python2.7/site-packages:$PYTHONPATH
