#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/env.sh
cd $DIR

#run the database server
redis-server redis.conf > server.log &

#submit jobs
for i in `seq 1 200`; do
    qsub -N rq_worker -wd $DIR -o $DIR/logs/ -e $DIR/logs/ worker.sh
done

