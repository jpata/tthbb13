#!/bin/bash
fts-transfer-status -s https://fts3-pilot.cern.ch:8443 -l $1 | grep State | sort | uniq -c
