#!/bin/bash
set -e

#GNU parallel
PARCMD=~joosep/parallel

#list of input files
SRCFILE=$2

#directory under which to save output, will be created
DSTDIR=`mktemp -d`
DSTFILE=$1

#first pass, 10 files per hadd
rm -Rf $DSTDIR/step1
mkdir -p $DSTDIR/step1
echo "step1"
cat $SRCFILE | $PARCMD -n10 hadd $DSTDIR/step1/merged_{#}.root {}

#second pass, 5 files per hadd
rm -Rf $DSTDIR/step2
mkdir -p $DSTDIR/step2
echo "step2"
find $DSTDIR/step1 -name "merged_*.root" | $PARCMD -n5 hadd $DSTDIR/step2/merged_{#}.root {}

#final pass, hadd all
rm -f $DSTDIR/merged.root
echo "step3"
hadd $DSTDIR/merged.root $DSTDIR/step2/merged_*.root
rm -Rf $DSTDIR/step1
rm -Rf $DSTDIR/step2

#move final file
mv $DSTDIR/merged.root $DSTFILE

#output is at $DSTDIR/merged.root
du -csh $DSTFILE

#cleanup
rm -Rf $DSTDIR
