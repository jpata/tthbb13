#!/bin/bash
source env.sh
env
cd $SGE_O_WORKDIR
rq worker -c settings
