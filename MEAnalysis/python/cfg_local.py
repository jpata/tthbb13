from TTH.MEAnalysis.MEAnalysis_cfg_heppy import Conf
import os

Conf.general["sampleFile"] = os.environ["CMSSW_BASE"] + "/src/TTH/MEAnalysis/python/samples_local.py"
calcME = int(os.environ.get("TTH_CALCME", 0))
if calcME == 1:
    calcME = True
else:
    calcME = False
Conf.mem["calcME"] = calcME
