#!/bin/bash

# Get private environment variables
echo "Reading env.sh:"
cat env.sh
source env.sh
echo "Done reading env.sh:"
source common.sh

#print out the environment
env
set -e


#go to work directory
cd $MY_SCRATCH

# Create output directory
mkdir out

echo "Running MakeCategory"
echo ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeCategory.py $sparsefile $specfile $analysis $category
python ${CMSSW_BASE}/src/TTH/Plotting/python/Datacards/MakeCategory.py $sparsefile $specfile $analysis $category
echo "Done MakeCategory"

#copy output
OUTDIR=$HOME/tth/gc/makecategory/${TASK_ID}/${analysis}/
mkdir -p $OUTDIR 
echo "copying output"
cp $category.root $OUTDIR 
cp shapes_${category}*.txt $OUTDIR 



