#!/bin/bash
HOSTNAME=`hostname`
PORT=$1

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/env.sh
cd $DIR

echo "bind $HOSTNAME" > redis.conf
echo "port $PORT" >> redis.conf
echo "REDIS_URL = 'redis://$HOSTNAME:$PORT'" > settings.py

#run the database server
redis-server redis.conf
