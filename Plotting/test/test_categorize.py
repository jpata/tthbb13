import unittest
 
from TTH.Plotting.Datacards import Categorize
from TTH.Plotting.Datacards import Cut
from TTH.Plotting.Datacards.makeDatacard import MakeDatacard2
from multiprocessing import Pool
from TTH.Plotting.Datacards.CombineHelper import LimitGetter, DummyLimitGetter

import os, ROOT

def make_tree():
        s = """
  Discr=mem_SL_0w2h2t
    numJets__4__5 Discr=mem_SL_0w2h2t 
       nBCSVM__3__4 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
    numJets__5__8 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
       numJets__6__8 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__8 Discr=mem_SL_0w2h2t
"""

        h_sig, h_bkg, h_sig_sys, h_bkg_sys = Categorize.GetSparseHistograms(
            "/home/joosep/joosep-mac/Dropbox/tth/ControlPlotsSparse.root",
            ["ttH_hbb"],
            [
                "ttbarPlus2B",
                "ttbarPlusB",
                "ttbarPlusBBbar",
                "ttbarPlusCCbar",
                "ttbarOther"
            ],
            "sl"
        )
        axes = Categorize.GetAxes(h_sig["ttH_hbb"])
        Cut.Cut.axes = axes
        Categorize.Categorization.axes = axes
        Categorize.Categorization.h_sig = h_sig
        Categorize.Categorization.h_bkg = h_bkg
        Categorize.Categorization.h_sig_sys = h_sig_sys
        Categorize.Categorization.h_bkg_sys = h_bkg_sys
        Categorize.Categorization.output_path = "./"
        Categorize.Categorization.pool = Pool(4)
        Categorize.Categorization.lg = LimitGetter(Categorize.Categorization.output_path)

        ret = Categorize.CategorizationFromString(s)
        assert(len(ret.children) == 2)
        return ret

class CategorizeTest(unittest.TestCase):
    def test_make_tree(self):
        make_tree()

class CategorizeMakeControlPlotTest(unittest.TestCase):
    def setUp(self):
        self.categorize = make_tree()
    
    def test_create_control_plots_split(self):
        self.categorize.create_control_plots("./", False)
        for f in self.categorize.leaf_files.items():
            assert(os.path.isfile(f[1]))
            tf = ROOT.TFile(f[1])
            assert(not tf is None)
    
    def test_create_control_plots_nosplit(self):
        self.categorize.create_control_plots("./", True)
        print "test_create_control_plots_nosplit", self.categorize.leaf_files

    def test_getProcesses(self):
        assert(self.categorize.getProcesses() == ['ttH_hbb', 'ttbarPlusBBbar', 'ttbarPlusCCbar', 'ttbarPlus2B', 'ttbarPlusB', 'ttbarOther'])
    
    def test_get_leaves(self):
        leaves = self.categorize.get_leaves()
        print leaves
        lnames = [
            'numJets__3__5__nBCSVM__2__4__discr_mem_SL_0w2h2t',
            'numJets__3__5__nBCSVM__4__5__discr_mem_SL_0w2h2t',
            'numJets__3__6__nBCSVM__2__4__discr_mem_SL_0w2h2t',
            'numJets__3__6__nBCSVM__4__5__discr_mem_SL_0w2h2t',
            'numJets__6__7__nBCSVM__2__3__discr_mem_SL_0w2h2t',
            'numJets__6__7__nBCSVM__3__5__discr_mem_SL_0w2h2t',
            'numJets__6__7__nBCSVM__4__5__discr_mem_SL_0w2h2t'
        ]
        for leaf in leaves:
            p = lnames.pop(lnames.index(leaf.__repr__()))
        assert(len(lnames) == 0)
    
    
    def test_getLeafDiscriminators(self):
        leaf_disc = self.categorize.getLeafDiscriminators(False)
        leaves = self.categorize.get_leaves(False)
        for leaf in leaves:
            leaf_disc[leaf.__repr__()] == leaf.discriminator_axis
    
    def test_make_datacard(self):
        self.categorize.create_control_plots("./", False)
        MakeDatacard2(
            self.categorize,
            self.categorize.leaf_files,
            "shapes.txt",
            do_stat_variations=Categorize.Categorization.do_stat_variations
        )
    
    def test_find_categories_async(self):
        cut_axes = ["topCandidate_mass"]
        discriminator_axes = ["mem_SL_0w2h2t"]
        for l in self.categorize.get_leaves()[:2]:
            print "Optimizing leaf", l
    
            #for left-handed child (bg-like), don't use MEM discriminator, just a counting experiment
            l.disc_axes_child_left = ["counting"]
            l.find_categories_async(
                1,
                cut_axes,
                discriminator_axes
            )
            print l, l.cut
 
    def test_print_tree_latex(self):
        print "printing tree"
        tree = self.categorize.print_tree_latex()
        print tree

if __name__ == "__main__":
    unittest.main()
