import subprocess
import copy, os
import unittest
import logging
import ROOT

class MEAnalysisTestCase(unittest.TestCase):
    testfiles = [
        ("/store/user/jpata/tth/tth_Jul31_V24_v1/ttHTobb_M125_13TeV_powheg_pythia8/tth_Jul31_V24_v1/160731_130548/0000/tree_1.root", "signal"),
    ]
    
    def test_MEAnalysis(self):
        infile = "/store/user/jpata/tth/tth_Jul31_V24_v1/ttHTobb_M125_13TeV_powheg_pythia8/tth_Jul31_V24_v1/160731_130548/0000/tree_1.root"
        env = copy.copy(os.environ)
        CMSSW_BASE = os.environ["CMSSW_BASE"]
        env["ME_CONF"] = os.path.join(CMSSW_BASE, "src/TTH/MEAnalysis/python/cfg_local.py")
        env["INPUT_FILE"] = infile
        ret = subprocess.Popen([
            "python", "MEAnalysis/python/MEAnalysis_heppy.py",
        ], env=env).communicate()
        return True

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
