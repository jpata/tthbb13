#!/bin/bash

exitCode=$1
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
