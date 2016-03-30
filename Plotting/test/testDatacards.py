import ROOT, rootpy
import unittest
from collections import OrderedDict

import TTH.Plotting.Datacards.sparse as sparse
from datasets import data, open_data


import TTH.Plotting.Datacards.AnalysisSpecification as anspec
import TTH.Plotting.Datacards.MakeCategory as MakeCategory
import TTH.Plotting.Datacards.utils as utils


class SparseToolsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.file = open_data(data["sparse"])
        cls.hsparse = cls.file.Get("ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb/sl/sparse")
    
    @classmethod
    def tearDownClass(cls):
        cls.file.Close()

    def test_find_axis_success(self):
        self.assertEqual(sparse.find_axis(self.hsparse, "numJets"), 8)

    def test_find_axis_fail(self):
        def f():
            sparse.find_axis(self.hsparse, "asdf")
        self.assertRaises(KeyError, f)

    def test_set_range(self):
        iax = sparse.find_axis(self.hsparse, "numJets")

        sparse.set_range(self.hsparse, "numJets", 0, 20)
        h1 = self.hsparse.Projection(iax).Clone("p1")

        sparse.set_range(self.hsparse, "numJets", 0, 6)
        h2a = self.hsparse.Projection(iax).Clone("p2a")

        sparse.set_range(self.hsparse, "numJets", 6, 10)
        h2b = self.hsparse.Projection(iax).Clone("p2b")

        self.assertAlmostEqual(h1.Integral(), h2a.Integral()+h2b.Integral())

    def test_apply_cuts_project_1d(self):
        h1 = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        #self.assertIsInstance(h1, rootpy.plotting.hist.Hist)
        self.assertAlmostEqual(h1.Integral(), 179578.0055940163)
        self.assertEqual(h1.GetName(), "numJets__4__6__nBCSVM__1__3__btag_LR_4b_2b_logit")

    def test_apply_cuts_project_2d(self):
        h1 = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 100)], ["btag_LR_4b_2b_logit", "common_bdt"])
        #self.assertIs(type(h1), rootpy.plotting.hist.Hist2D)
        self.assertAlmostEqual(h1.Integral(), 256605.17045173675)
        self.assertEqual(h1.GetName(), "numJets__4__6__nBCSVM__1__100__btag_LR_4b_2b_logit__common_bdt")

    def test_save_hdict(self):
        h1 = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        h2 = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 3, 6)], ["btag_LR_4b_2b_logit"])
        hdict = OrderedDict()
        hdict["ttH_hbb/cat1/blr/hblr"] = h1.Clone("hblr")
        hdict["ttH_hbb/cat2/blr/hblr_asd"] = h2.Clone("hblr_asd")
        sparse.save_hdict("test.root", hdict)
        
        inf = rootpy.io.File("test.root")
        h1a = inf.Get("ttH_hbb/cat1/blr/hblr")
        self.assertIsNot(h1a, None)
        self.assertEqual(h1a.Integral(), h1.Integral())

        h2a = inf.Get("ttH_hbb/cat2/blr/hblr_asd")
        self.assertIsNot(h2a, None)
        self.assertEqual(h2a.Integral(), h2.Integral())
        inf.close()

    def test_save_hdict_dupe(self):
        ROOT.TH1F.AddDirectory(False)
        h1 = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["Wmass"])
        h2 = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 3, 6)], ["common_bdt"])
        hdict = OrderedDict()
        hdict["data/dl_jge4_tge4/Wmass"] = h1.Clone()
        hdict["data/dl_jge4_tge4/common_bdt"] = h2.Clone()
        sparse.save_hdict("test.root", hdict)
        
        inf = rootpy.io.File("test.root")
        h1a = inf.Get("data/dl_jge4_tge4/Wmass")
        self.assertIsNot(h1a, None)
        self.assertEqual(h1a.Integral(), h1.Integral())
        
        h2a = inf.Get("data/dl_jge4_tge4/common_bdt")
        self.assertIsNot(h2a, None)
        self.assertEqual(h2a.Integral(), h2.Integral())
        inf.close()
    
    def test_save_hdict_many(self):
        ROOT.TH1F.AddDirectory(False)
        h1 = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        hdict = OrderedDict()
        for i in range(1000):
            hdict["ttH_hbb/cat{0}/hblr".format(i)] = h1.Clone("h{0}".format(i))
        sparse.save_hdict("test.root", hdict)

    def test_add_hdict(self):
        ROOT.TH1F.AddDirectory(False)
        hd1 = {}
        hd1["ttH_hbb/cat1/hblr"] = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        hd1["ttH_hbb/cat2/hblr"] = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 3, 4)], ["btag_LR_4b_2b_logit"])

        hd2 = {}
        hd2["ttH_hbb/cat1/hblr"] = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 1, 3)], ["btag_LR_4b_2b_logit"])
        hd2["ttH_hbb/cat3/hblr"] = sparse.apply_cuts_project(self.hsparse, [("numJets", 4, 6), ("nBCSVM", 3, 4)], ["btag_LR_4b_2b_logit"])

        hd = sparse.add_hdict(hd1, hd2)
        
        self.assertEqual(
            hd["ttH_hbb/cat1/hblr"].Integral(),
            hd1["ttH_hbb/cat1/hblr"].Integral() + hd2["ttH_hbb/cat1/hblr"].Integral()
        )

        self.assertEqual(
            hd["ttH_hbb/cat2/hblr"].Integral(),
            hd1["ttH_hbb/cat2/hblr"].Integral()
        )

        self.assertEqual(
            hd["ttH_hbb/cat3/hblr"].Integral(),
            hd2["ttH_hbb/cat3/hblr"].Integral()
        )

class MakeCategoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = open_data(data["sparse"])
        cls.hsparse = cls.file.Get("ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb/sl/sparse")
        cls.analysis = anspec.analysis

    @classmethod
    def tearDownClass(cls):
        cls.file.Close()

    def test_Sample(self):
        samp = anspec.Sample(
            input_name = "ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb",
            output_name = "ttH_hbb",
            cuts = [("numJets", 6, 8)]
        )
        self.assertEqual(samp.input_name, "ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb")
        self.assertEqual(samp.output_name, "ttH_hbb")
        self.assertEqual(samp.cuts, [("numJets", 6, 8)])

    def step_Category(self):
        samps = [
            anspec.Sample(
                input_name = "ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb",
                output_name = "ttH_hbb",
            ),
            anspec.Sample(
                input_name = "TT_TuneCUETP8M1_13TeV-powheg-pythia8/ttbarPlusBBbar",
                output_name = "ttbarPlusBBbar",
            )
        ]
        common_shape_uncertainties = {
            "CMS_scale_j": 1.0,
        }
        shape_uncertainties = {
            "ttH_hbb": {
                "CMS_ttH_CSVHF": 2.0
            }
        }
        cat = anspec.Category(
            name = "sl_jge6_tge4",
            cuts = [("numJets", 6, 8), ("nBCSVM", 4, 8)],
            samples = samps,
            signal_processes = ["ttH_hbb"],
            common_shape_uncertainties = common_shape_uncertainties,
            common_scale_uncertainties = {},
            scale_uncertainties = {},
            shape_uncertainties = shape_uncertainties,
            discriminator = "mem_SL_0w2h2t",
            src_histogram = "sl/sparse"
        )
        self.cat = cat
        self.assertTrue(cat.shape_uncertainties.has_key("ttH_hbb"))
        self.assertTrue(cat.shape_uncertainties.has_key("ttbarPlusBBbar"))
        self.assertFalse(cat.shape_uncertainties.has_key("ttH_nonbb"))
        self.assertTrue(cat.shape_uncertainties["ttH_hbb"].has_key("CMS_scale_j"))
        self.assertEquals(cat.shape_uncertainties["ttH_hbb"]["CMS_scale_j"], 1.0)
        self.assertEquals(cat.shape_uncertainties["ttH_hbb"]["CMS_ttH_CSVHF"], 2.0)
        self.assertFalse(cat.shape_uncertainties["ttbarPlusBBbar"].has_key("CMS_ttH_CSVHF"))

        self.assertIn("ttH_hbb", cat.processes)
        self.assertIn("ttbarPlusBBbar", cat.processes)
        self.assertNotIn("ttH_nonbb", cat.processes)

    def step_make_rules(self):
        rules = []
        rules += MakeCategory.make_rule_cut(self.cat.src_histogram, self.cat)

        passSystName = False
        for rule in rules:
            if (rule["input"] == "ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb/sl/sparse_CMS_scale_jUp" and
                rule["cuts"] == "[('numJets', 6, 8), ('nBCSVM', 4, 8)]"):
                passSystName = rule["output"] == "ttH_hbb/sl_jge6_tge4/mem_SL_0w2h2t_CMS_scale_jUp"

        self.assertTrue(passSystName)
        self.rules = rules

    def step_apply_rules(self):
        hdict = MakeCategory.apply_rules_parallel(self.file.GetName(), self.rules)

        self.assertTrue(hdict.has_key("ttH_hbb/sl_jge6_tge4/mem_SL_0w2h2t"))
        self.assertTrue(hdict.has_key("ttH_hbb/sl_jge6_tge4/mem_SL_0w2h2t_CMS_ttH_CSVHFUp"))
        self.assertTrue(hdict.has_key("ttbarPlusBBbar/sl_jge6_tge4/mem_SL_0w2h2t_CMS_scale_jDown"))
        

        self.assertTrue(hdict["ttH_hbb/sl_jge6_tge4/mem_SL_0w2h2t"].Integral() > 0)
        self.assertTrue(hdict["ttH_hbb/sl_jge6_tge4/mem_SL_0w2h2t_CMS_ttH_CSVHFUp"].Integral() > 0)
        self.assertTrue(hdict["ttbarPlusBBbar/sl_jge6_tge4/mem_SL_0w2h2t_CMS_scale_jDown"].Integral() > 0)
        self.hdict = hdict

    def step_fake_data(self):
        hfile = "test.root"
        sparse.save_hdict(hfile, self.hdict)
        tf = ROOT.TFile(hfile, "UPDATE")
        utils.fakeData(tf, tf, [self.cat])
        tf.Close()

        tf = ROOT.TFile(hfile)
        h = tf.Get("data_obs/sl_jge6_tge4/mem_SL_0w2h2t")
        self.assertFalse(h is None)
        self.assertEquals(
            h.Integral(),
            tf.Get("ttH_hbb/sl_jge6_tge4/mem_SL_0w2h2t").Integral() +
            tf.Get("ttbarPlusBBbar/sl_jge6_tge4/mem_SL_0w2h2t").Integral()
        )

    def step_stat_variations(self):
        hfile = "test.root"
        tf = ROOT.TFile(hfile, "UPDATE")
        stathist_names = utils.makeStatVariations(tf, tf, [self.cat])
        self.assertTrue(stathist_names.has_key("sl_jge6_tge4"))
        self.assertTrue(stathist_names["sl_jge6_tge4"].has_key("ttbarPlusBBbar"))
        self.assertIn("ttbarPlusBBbar_sl_jge6_tge4_Bin1", stathist_names["sl_jge6_tge4"]["ttbarPlusBBbar"])
        tf.Close()

    def test_A(self):
        self.step_Category()

    def test_B(self):
        self.step_Category()
        self.step_make_rules()

    def test_C(self):
        self.step_Category()
        self.step_make_rules()
        self.step_apply_rules()

    def test_D_fakeData(self):
        self.step_Category()
        self.step_make_rules()
        self.step_apply_rules()
        self.step_fake_data()

    def test_E_statVariations(self):
        self.step_Category()
        self.step_make_rules()
        self.step_apply_rules()
        self.step_fake_data()
        self.step_stat_variations()

class DatacardUtilsTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.file = open_data(data["sparse"])
        cls.hsparse = cls.file.Get("ttHTobb_M125_13TeV_powheg_pythia8/ttH_hbb/sl/sparse")
        
    @classmethod
    def tearDownClass(cls):
        cls.file.Close()

def main():
    unittest.main()

if __name__ == "__main__":
    main()
