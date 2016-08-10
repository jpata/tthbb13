#!/usr/bin/env python
"""
Simple test runner for the workflow scripts.
"""
import subprocess
import copy, os
import unittest
import logging

class MEAnalysisTestCase(unittest.TestCase):
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

def run_sparsinator(infiles, datasetpath):
    print "running on files", infiles
    env = copy.copy(os.environ)
    CMSSW_BASE = os.environ["CMSSW_BASE"]
    env["FILE_NAMES"] = " ".join(infiles)
    env["DATASETPATH"] = datasetpath
    ret = subprocess.Popen([
        "python", "Plotting/python/joosep/sparsinator.py",
    ], env=env).communicate()
    return

def read_inputs(dataset):
    fi = open(dataset)
    lines = [x.split()[0].strip() for x in fi.readlines() if ".root" in x]
    return lines

class MakeSparsinatorTestCase(unittest.TestCase):
    def test_sparsinator_data(self):
        run_sparsinator(read_inputs("MEAnalysis/gc/datasets/tth_Jul31_V24_v1/SingleMuon.txt")[:2], "SingleMuon")
        
        self.assertTrue(os.path.isfile("out.root"))
        fi = ROOT.TFile("out.root")
        hi = fi.Get("ttHTobb_M125_13TeV_powheg_pythia8/sl/sparse")
        self.assertFalse(hi == None)
        fi.Close()
    
    def test_sparsinator_mc(self):
        run_sparsinator(read_inputs("MEAnalysis/gc/datasets/tth_Jul31_V24_v1/ttHTobb_M125_13TeV_powheg_pythia8.txt")[:1], "ttHTobb_M125_13TeV_powheg_pythia8")
        
        self.assertTrue(os.path.isfile("out.root"))
        fi = ROOT.TFile("out.root")
        hi = fi.Get("ttHTobb_M125_13TeV_powheg_pythia8/sl/sparse")
        self.assertFalse(hi == None)
        fi.Close()

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
        
        import ROOT
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
    logging.basicConfig(level=logging.INFO)

    #test_MEAnalysis("/store/user/jpata/tth/tth_Jul31_V24_v1/ttHTobb_M125_13TeV_powheg_pythia8/tth_Jul31_V24_v1/160731_130548/0000/tree_1.root")
    #test_sparsinator(read_inputs("MEAnalysis/gc/datasets/tth_Jul31_V24_v1/SingleMuon.txt")[:5], "SingleMuon")
    #test_sparsinator(read_inputs("MEAnalysis/gc/datasets/tth_Jul31_V24_v1/ttHTobb_M125_13TeV_powheg_pythia8.txt")[:5], "ttHTobb_M125_13TeV_powheg_pythia8.txt")
    #test_MakeCategory("sl_jge6_tge4")
    unittest.main()
