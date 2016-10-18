import subprocess
import copy, os
import unittest
import logging
import ROOT

from TTH.Plotting.Datacards.MakeCategory import get_categories

class MakeCategoryTestCase(unittest.TestCase):
    
    def launch_MakeCategory_test(self,catname,analysis, var):
        from TTH.Plotting.Datacards.MakeCategory import main as MakeCategory_main

        anspec = os.path.join(
            os.environ["CMSSW_BASE"],
            "src/TTH/Plotting/python/Datacards/AnalysisSpecification.py"
        )

        analysis, categories = get_categories(anspec, "FH", catname)
        MakeCategory_main(analysis, categories)
        outfile = "{0}.root".format(catname)
        self.assertTrue(os.path.isfile(outfile))
        
        fi = ROOT.TFile(outfile)
        self.assertFalse(fi == None)

        for samp in ["ttH_hbb", "data", "data_obs"]:
            hname = "{0}/{1}/{2}".format(samp, catname, var)
            logging.debug("test_MakeCategory_run: getting {0}".format(hname))
            h = fi.Get(hname)
            logging.debug("test_MakeCategory_run: {0} integral={1}".format(hname, h.Integral()))
            self.assertFalse(h == None)
            self.assertTrue(h.Integral() > 0.0)

    def test_MakeCategory_run_FH(self):
        self.launch_MakeCategory_test("fh_j8_t4","FH","jetsByPt_0_pt")

'''    
    def test_MakeCategory_run_SL(self):
        self.launch_MakeCategory_test("sl_jge6_tge4","SL_7cat","jetsByPt_0_pt")
'''


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
