#!/bin/bash
qdel -u tklijnsm
rm -rf work.bkg
rm -rf work.sig
python tthbb.py --action=submit
python tthbb.py --action=status
