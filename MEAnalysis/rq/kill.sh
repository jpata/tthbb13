#!/bin/bash
JOBS=`qstat -u jpata | grep "rq_worker" | awk '{print $1}' | xargs`
qdel $JOBS
