echo "Hello World!"

ls -lactrh src/TTH/TTHNtupleAnalyzer/data/*UncertaintySources*

# Put the UncertaintySources in a few places to make sure the NTupelize fins it
cp -v src/TTH/TTHNtupleAnalyzer/data/*UncertaintySources* .
cp -v src/TTH/TTHNtupleAnalyzer/data/*UncertaintySources* src/
cp -v src/TTH/TTHNtupleAnalyzer/data/*UncertaintySources* ${CMSSW_VERSION}
cp -v src/TTH/TTHNtupleAnalyzer/data/*UncertaintySources* ${CMSSW_VERSION}/src
cp -v src/TTH/TTHNtupleAnalyzer/data/*UncertaintySources* ${CMSSW_VERSION}/external/slc6_amd64_gcc491/data

echo "ls -lactrh"
ls -lactrh

echo "ls -lactrh *"
ls -lactrh *

echo "pwd"
pwd

echo "Extending CMSSW SEARCH PATH"
export CMSSW_SEARCH_PATH=$PWD:$CMSSW_SEARCH_PATH
export CMSSW_SEARCH_PATH=$PWD/src:$CMSSW_SEARCH_PATH
export CMSSW_SEARCH_PATH=$PWD/src/TTH/TTHNtupleAnalyzer/data:$CMSSW_SEARCH_PATH
echo "CMSSW_SEARCH_PATH="
echo $CMSSW_SEARCH_PATH

echo "LD_LIBRARY_PATH="
echo $LD_LIBRARY_PATH   

echo "export"
export LD_LIBRARY_PATH=$PWD/lib/slc6_amd64_gcc491/:$LD_LIBRARY_PATH

echo "LD_LIBRARY_PATH="
echo $LD_LIBRARY_PATH   

# Actually, let's do something more useful than a simple hello world... this will print the input arguments passed to the script
echo "Here there are all the input arguments"
echo $@

# If you are curious, you can have a look at the tweaked PSet. This however won't give you any information...
echo "================= PSet.py file =================="
cat PSet.py

# This is what you need if you want to look at the tweaked parameter set!!
echo "================= Dumping PSet ===================="
python -c "import PSet; print PSet.process.dumpPython()"

# Ok, let's stop fooling around and execute the job:
cmsRun -j FrameworkJobReport.xml -p PSet.py

echo "Done with cmsRun"

echo "Doing ls"
ls -lactrh .

#echo "Running MakeTaggingNtuple.py"
#python MakeTaggingNtuple.py
#echo "Done with MakeTaggingNtuple.py"

echo "Doing ls"
ls -lactrh .

