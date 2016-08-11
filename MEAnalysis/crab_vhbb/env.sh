#!/bin/bash
echo "heppy_crab_script_pre.sh"

tar xvzf python.tar.gz --directory $CMSSW_BASE 
tar xzf data.tar.gz --directory $CMSSW_BASE/src/TTH/MEAnalysis
echo "ENV"
env
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd"
echo $CMSSW_BASE
echo $PYTHON_PATH
echo $PWD
cp -r lib/slc*/* $CMSSW_BASE/lib/slc*
cp -r lib/slc*/.* $CMSSW_BASE/lib/slc*
echo "AFTER COPY content of $CMSSW_BASE/lib/slc*"

cp -r interface/* $CMSSW_BASE/interface/
echo "AFTER COPY content of $CMSSW_BASE/interface"

cp -r src/* $CMSSW_BASE/src/
echo "AFTER COPY content of $CMSSW_BASE/src"

PROXYFILE=`grep "BEGIN CERTIFICATE" * | perl -pe 's/:.*//'  | grep -v heppy | tail -n 1`
export X509_USER_PROXY=$PWD/$PROXYFILE
echo Found Proxy in: $X509_USER_PROXY
MD5SUM=`cat python.tar.gz heppy_config.py | md5sum | awk '{print $1}'`

cat <<EOF > fakeprov.txt
Processing History:
 HEPPY '' '"CMSSW_X_y_Z"' [1]  ($MD5SUM)
EOF

cat <<EOF > $CMSSW_BASE/bin/$SCRAM_ARCH/edmProvDump
#!/bin/sh
cat fakeprov.txt
EOF

chmod +x $CMSSW_BASE/bin/$SCRAM_ARCH/edmProvDump

echo "Which edmProvDump"
which edmProvDump
edmProvDump

# Update library path
# Needed so recompiled modules are found
#export LD_LIBRARY_PATH=./lib/slc6_amd64_gcc481:$LD_LIBRARY_PATH 
cd $CMSSW_BASE
eval `scram runtime -sh`
cd -
echo "LD LIBRARY PATH IS"
echo $LD_LIBRARY_PATH

export ROOT_INCLUDE_PATH=.:./src:$ROOT_INCLUDE_PATH

echo "tth_hashes"
cat hash

# Use version from IB until it migrates to the main release
# Should work as long as both releases have same python version
# Will need to update this path once in a while
export IB_BASE=/cvmfs/cms-ib.cern.ch/week0/slc6_amd64_gcc530
export PYTHONPATH=$IB_BASE/external/py2-numpy/1.11.1/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-scikit-learn/0.17.1/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-pandas/0.17.1-agcabg/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-matplotlib/1.5.2/lib/python2.7/site-packages:$PYTHONPATH
export PYTHONPATH=$IB_BASE/external/py2-scipy/0.16.1/lib/python2.7/site-packages:$PYTHONPATH

echo "Our NEW PYTHONPATH:"
echo $PYTHONPATH

echo "ls /cvmfs/"
ls /cvmfs/

echo "ls /cvmfs/cms-ib.cern.ch/"
ls /cvmfs/cms-ib.cern.ch/

echo "ls /cvmfs/cms-ib.cern.ch/week0/"
ls /cvmfs/cms-ib.cern.ch/week0/

echo "ls /cvmfs/cms-ib.cern.ch/week0/slc6_amd64_gcc530"
ls /cvmfs/cms-ib.cern.ch/week0/slc6_amd64_gcc530

echo "ls /cvmfs/cms-ib.cern.ch/week0/slc6_amd64_gcc530/external"
ls /cvmfs/cms-ib.cern.ch/week0/slc6_amd64_gcc530/external

echo "ls /cvmfs/cms-ib.cern.ch/week0/slc6_amd64_gcc530/external/py2-scikit-learn"
ls /cvmfs/cms-ib.cern.ch/week0/slc6_amd64_gcc530/external/py2-scikit-learn
