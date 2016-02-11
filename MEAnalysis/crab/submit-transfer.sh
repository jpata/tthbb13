#!/bin/bash
fts-transfer-submit --retry 100 --retry-delay 120 -s https://fts3-pilot.cern.ch:8443 -f $1 > $1.transfer-id
