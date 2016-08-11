#s -lR
echo "heppy_crab_script_data.sh"
tar xvzf python.tar.gz --directory $CMSSW_BASE 
tar xzf data.tar.gz --directory $CMSSW_BASE/src/TTH/MEAnalysis
echo "ENV..................................."
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
cp heppy_config_data.py heppy_config.py
python heppy_crab_script.py $@ &> log
exitCode=$?
cat log

if [ $exitCode -eq 0 ]; then
echo "command succeeded"
else
cat log | python analyze_log.py
exitCode=$?
errorType=""
exitMessage=`tail -n500 | grep -A5 -B5 -i error`
cat << EOF > FrameworkJobReport.xml
<FrameworkJobReport>
<FrameworkError ExitStatus="$exitCode" Type="$errorType" >
$exitMessage
</FrameworkError>
</FrameworkJobReport>
EOF
fi

tail -n500 log
cat FrameworkJobReport.xml
echo "======================== CMSRUN LOG ============================"
head -n 500 Output/cmsRun.log 
echo "=== SNIP ==="
tail -n 500 Output/cmsRun.log 
