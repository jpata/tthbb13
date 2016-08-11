import subprocess
import copy, os
import unittest
import logging
import ROOT

class MakeCategoryTestCase(unittest.TestCase):
    
    def test_MakeCategory_run(self):
        from TTH.Plotting.Datacards.MakeCategory import main as MakeCategory_main
        catname = "sl_jge6_tge4"
        MakeCategory_main(
            os.path.join(
                os.environ["CMSSW_BASE"],
                "src/TTH/Plotting/python/Datacards/AnalysisSpecificationSL.py",
            ),
            "SL_7cat",
            catname
        )
        outfile = "{0}.root".format(catname)
        self.assertTrue(os.path.isfile(outfile))
        
        fi = ROOT.TFile(outfile)
        self.assertFalse(fi == None)

        for samp in ["ttH_hbb", "data", "data_obs", "ttbarOther"]:
            hname = "{0}/{1}/jetsByPt_0_pt".format(samp, catname)
            logging.debug("test_MakeCategory_run: getting {0}".format(hname))
            h = fi.Get(hname)
            logging.debug("test_MakeCategory_run: {0} integral={1}".format(hname, h.Integral()))
            self.assertFalse(h == None)
            self.assertTrue(h.Integral() > 0.0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
