#!/bin/bash
WD=`pwd`
for i in `seq 1 300`; do
    qsub -q all.q -N rq_worker -wd $WD -o $WD/logs/ -e $WD/logs/ worker.sh
done
