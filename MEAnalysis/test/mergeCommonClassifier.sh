#!/bin/bash
python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep22_v1_ttH_nonhbb --outfile ttH_nonhbb.root
python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep22_v1_ttH_hbb --outfile ttH_hbb.root
python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep22_v1_ttjetsUnsplit --outfile ttjetsUnsplit.root
python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep22_v1_ttjets_sl_t --outfile ttjets_sl_t.root
python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep22_v1_ttjets_sl_tbar --outfile ttjets_sl_tbar.root
