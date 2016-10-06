#!/bin/bash
set +e

#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_ttH_nonhbb --outfile ttH_nonhbb.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_ttH_hbb --outfile ttH_hbb.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_ttjetsUnsplit --outfile ttjetsUnsplit.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_data_m --outfile data_m.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_data_e --outfile data_e.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_data_mm --outfile data_mm.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_data_em --outfile data_em.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_data_ee --outfile data_ee.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_ttjets_sl_t --outfile ttjets_sl_t.root
#python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/CRAB_UserFiles/crab_MEM_Sep29_ETH_v1_ttjets_sl_tbar --outfile ttjets_sl_tbar.root

FILES="
crab_MEM_DESY_Oct5_ttbarH125tobbbar
"

for f in $FILES
do
    python remote_hadd.py --server storage01.lcg.cscs.ch --path /pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/mem/DESY_Oct5/CRAB_UserFiles/$f --outfile $f.root
done


