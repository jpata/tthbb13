echo "tthbb crab script started"
#s -lR
tar xzf python.tar.gz --directory $CMSSW_BASE 
tar xzf data.tar.gz --directory $CMSSW_BASE/src/TTH/MEAnalysis 
#ls -lR .
echo "ENV..................................."
env 
#echo "VOMS"
#voms-proxy-info -all
#echo "CMSSW BASE, python path, pwd"
#echo $CMSSW_BASE 
#echo $PYTHON_PATH
#echo $PWD 
cp lib/slc*/* $CMSSW_BASE/lib/slc*
cp lib/slc*/.* $CMSSW_BASE/lib/slc*
echo "AFTER COPY content of $CMSSW_BASE/lib/slc*"
#ls -lR  $CMSSW_BASE/lib/slc*
#
cp -r interface/* $CMSSW_BASE/interface/
#echo "AFTER COPY content of $CMSSW_BASE/interface"
#ls -lR  $CMSSW_BASE/interface/
#
cp -r src/* $CMSSW_BASE/src/
#echo "AFTER COPY content of $CMSSW_BASE/src"
#ls -lR  $CMSSW_BASE/src/
#
#PROXYFILE=`grep "BEGIN CERTIFICATE" * | perl -pe 's/:.*//'  | grep -v heppy | tail -n 1`
#export X509_USER_PROXY=$PWD/$PROXYFILE
#echo Found Proxy in: $X509_USER_PROXY
MD5SUM=`cat python.tar.gz heppy_config.py | md5sum | awk '{print $1}'`
#
echo "making fake provenance"
cat <<EOF > fakeprov.txt
Processing History:
 HEPPY '' '"CMSSW_X_y_Z"' [1]  ($MD5SUM)
EOF

cat <<EOF > $CMSSW_BASE/bin/$SCRAM_ARCH/edmProvDump
#!/bin/sh
cat fakeprov.txt
EOF

chmod +x $CMSSW_BASE/bin/$SCRAM_ARCH/edmProvDump


#echo "Which edmProvDump"
#which edmProvDump
edmProvDump
#
## Update library path
## Needed so recompiled modules are found
export LD_LIBRARY_PATH=./lib/slc6_amd64_gcc491:$LD_LIBRARY_PATH 
#cd $CMSSW_BASE
#eval `scram runtime -sh`
#cd -
#echo "LD LIBRARY PATH IS"
#echo $LD_LIBRARY_PATH
#
#export ROOT_INCLUDE_PATH=.:./src:$ROOT_INCLUDE_PATH

echo "Running python code"
python heppy_crab_script.py $1
