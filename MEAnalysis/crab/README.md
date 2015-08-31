Submitting to grid
==================

The MEM workflow can be run over the grid using CRAB3 with the following steps.

0. Make sure the latest work (including *.pyc files) is compiled using `scram b` in the `src` directory.
1. Files need to be distributed so they can be accessed via xroot. This can be done using the data_replica.py script. Make sure that the files are always copied to the same LFN.
2. Job splitting is provided for crab via `split.py`, check `make split` for an example.
3. crab configurations can be made from the template `heppy_crab_cfg.py` using `make configs`.
4. `crab submit cfg_dataset.py` -> `crab status crab_projects_mem/crab_dataset` -> `crab resubmit crab_projects_mem/crab_dataset`
5. it is expected to see a fraction of 56/10040 errors from xrootd, currently we just need to resubmit in these cases.

Important notes
===============

1. your shell username and grid username MUST be the same.
