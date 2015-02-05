#!/bin/bash

for f in `cat dqm/inputs.txt`; do
	echo $f
	python python/produce_dqm.py $f dqm.root
	python python/inspect_dqm.py dqm.root
done

