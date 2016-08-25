#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/env.sh
cd $DIR
redis-server redis.conf | tee server.log
