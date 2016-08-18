#!/bin/bash
source env.sh
env
cd $SGE_O_WORKDIR
python ~jpata/anaconda/bin/rq worker -c settings
