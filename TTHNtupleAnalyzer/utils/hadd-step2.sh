#!/bin/bash
SDIR=~/tth/s1_nov19_3a4602f__s2_b7e13a1/
hadd -f /scratch/joosep/tth/step2/tthbb.root $SDIR/MEAnalysis_all_rec_std_TTHBB125_p*.root
hadd -f /scratch/joosep/tth/step2/ttjets.root $SDIR/MEAnalysis_all_rec_std_TTJets*.root
