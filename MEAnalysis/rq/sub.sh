#!/bin/bash
for i in `seq 1 500`; do
    qsub -N rq_worker -wd `pwd` -o `pwd`/logs/ -e `pwd`/logs/ worker.sh
done
