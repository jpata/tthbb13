########################################
# Imports
########################################

from multiprocessing import Pool

import ROOT

import Categorize
from Forest import trees
from CombineHelper import LimitGetter, DummyLimitGetter
from Axis import axis
from Cut import Cut

import pickle, os
########################################
# Configuration
########################################

#ControlPlotsSparse_2015_10_15_withBLR.root
input_file = "ControlPlotsSparseJan20ntp.root"
output_path = "/scratch/joosep/test/"
#input_file = "/dev/shm/joosep/ControlPlotsSparse_corr.root"
#output_path = "/dev/shm/joosep/categorization2/"

n_proc = 10
n_iter = 8

signals = [
    "ttH_hbb", 
#    "ttH_nohbb"
]

backgrounds = [
    "ttbarPlus2B",
    "ttbarPlusB",
    "ttbarPlusBBbar",
    "ttbarPlusCCbar",
    "ttbarOther",
#    "ttw_wlnu",       
#    "ttw_wqq",        
#    "ttz_zllnunu",    
#    "ttz_zqq",
]        


########################################
# Analysis helper functions
########################################

def split_leaves_by_BLR(original, disc="mem_SL_0w2h2t"):
    """ Attempt to optimize BLR splitting of classic analysis categories """

    r = Categorize.CategorizationFromString(original)
    initial_leaves = r.get_leaves()
    cut_axes = ["btag_LR_4b_2b_logit"]
    discriminator_axes = [disc] #MEM SL 022 axis
    for l in initial_leaves:
        print "Optimizing leaf", l

        #for left-handed child (bg-like), don't use MEM discriminator, just a counting experiment
        #l.disc_axes_child_left = ["counting"]
        l.find_categories_async(
            1,
            cut_axes,
            discriminator_axes
        )
    return r
# End of split_leaves_by_BLR

def run_opt(original,
    n_iters,
    cuts=["common_bdt", "btag_LR_4b_2b_logit"],
    discs=["mem_SL_0w2h2t", "common_bdt"]
    ):
    """ Attempt to optimize BLR splitting of classic analysis categories """

    r = Categorize.CategorizationFromString(original)
    initial_leaves = r.get_leaves()
    for l in initial_leaves:
        print "Optimizing leaf", l
        l.find_categories_async(
            n_iters,
            cuts,
            discs 
        )
    return r
# End of choose_discriminator

highpurity = [
    "numJets__6__7__nBCSVM__4__5__discr_mem_SL_0w2h2t",
    "numJets__6__7__nBCSVM__3__5__discr_mem_SL_0w2h2t",
    "numJets__3__6__nBCSVM__4__5__discr_mem_SL_0w2h2t",
    "numJets__3__5__nBCSVM__4__5__discr_mem_SL_0w2h2t"
]

def split_leaves_by_BLR_highpurity(original):
    """ Attempt to optimize BLR splitting of classic analysis categories """

    r = Categorize.CategorizationFromString(original)
    initial_leaves = r.get_leaves()
    cut_axes = ["btag_LR_4b_2b_logit", "Wmass"]
    discriminator_axes = ["mem_SL_0w2h2t"] #MEM SL 022 axis
    for l in initial_leaves:
        if not l.__repr__() in highpurity:
            continue
        print "Optimizing leaf", l

        #for left-handed child (bg-like), don't use MEM discriminator, just a counting experiment
        l.disc_axes_child_left = ["btag_LR_4b_2b_logit", "Wmass"]
        l.find_categories_async(
            1,
            cut_axes,
            discriminator_axes
        )
    return r
# End of split_leaves_by_BLR


def optimize(r):
    """ Further optimize a given tree r """    

    # TODO: something clever for boosted prereq - it can be
    # conditional on mass or other variables... For now we just
    # evaluate it for more events than we should - costs a bit in
    # computing but should be safe physics wise
    #axes[0].discPrereq = [Cut(3,3,3)]
    #axes[1].discPrereq = [Cut(3,3,3)]

    cut_axes = ["numJets", "nBCSVM", "btag_LR_4b_2b_logit", "Wmass"]
    discriminator_axes = ["mem_SL_2w2h2t"]
    
    r.find_categories_async(n_iter, 
                            cut_axes, 
                            discriminator_axes)    
# End of optimize


def make_latex(name):
    """ Get name of tree (in trees), produce the latex version and
    safe it to a tex file """
    
    print "make_latex", name
    Categorize.Categorization.output_path = output_path + "/" + name
    os.mkdir(Categorize.Categorization.output_path)
    r = Categorize.CategorizationFromString(trees[name])
    r.axes = Categorize.Categorization.axes

    #r.print_yield_table()
    of = open( name + ".tex","w")
    of.write(r.print_tree_latex())
    r.SaveControlPlots(name)
    of.close()
    of = open(name + ".pickle", "w")
    of.write(pickle.dumps(r))
    of.close()
# End of make_latex


if __name__ == "__main__":

    ########################################
    # Setup Categorization
    ########################################
    
    Categorize.Categorization.output_path = output_path
    Categorize.Categorization.pool = Pool(n_proc)
    Categorize.Categorization.do_stat_variations = True
    Categorize.Categorization.lg = LimitGetter(output_path)
    
    #SL
    #h_sig, h_bkg, h_sig_sys, h_bkg_sys = Categorize.GetSparseHistograms(
    h_sl = Categorize.GetSparseHistograms(
        input_file,
        signals,
        backgrounds,
        "sl"
    )
    axes = Categorize.GetAxes(h_sl[0]["ttH_hbb"])

    Cut.axes = axes
    Categorize.Categorization.axes = axes
    Categorize.Categorization.h_sig = h_sl[0]
    Categorize.Categorization.h_bkg = h_sl[1]
    Categorize.Categorization.h_sig_sys = h_sl[2]
    Categorize.Categorization.h_bkg_sys = h_sl[3]

    #ret = run_opt("old", 5, ["common_bdt", "btag_LR_4b_2b_logit"], ["common_bdt", "mem_SL_0w2h2t"])
    #of = open("old_opt.tex", "w")
    #of.write(r.print_tree_latex())
    #of.close()
    Categorize.Categorization.scaling = 0.5
    make_latex("old")
    make_latex("old_blrsplit")
    #Categorize.Categorization.scaling = 1.0
    #make_latex("old_parity")
    #make_latex("old_bdt")
    #make_latex("old_blrsplit_mem_bdt_parity")
    #make_latex("old_bdt_mem")
    #make_latex("old_bdt_mem_blrsplit")
    #make_latex("old_blrsplit_B")
    #make_latex("old_blrsplit_B_bdt")
    #make_latex("old_bdtsplit_A")
    #make_latex("old_bdtsplit_B")
  
    #DL
    h_dl = Categorize.GetSparseHistograms(
        input_file,
        signals,
        backgrounds,
        "dl"
    )
    axes = Categorize.GetAxes(h_dl[0]["ttH_hbb"])

    Cut.axes = axes
    Categorize.Categorization.axes = axes
    Categorize.Categorization.h_sig = h_dl[0]
    Categorize.Categorization.h_bkg = h_dl[1]
    Categorize.Categorization.h_sig_sys = h_dl[2]
    Categorize.Categorization.h_bkg_sys = h_dl[3]
    
    #Categorize.Categorization.scaling = 0.5
    #make_latex("old_dl")
    #make_latex("old_dl_blrsplit")
    #Categorize.Categorization.scaling = 1.0
    #make_latex("old_dl_parity")
    #Categorize.Categorization.output_path = output_path + "/old_dl_blr_opt"
    #os.mkdir(Categorize.Categorization.output_path)
    #r = split_leaves_by_BLR(trees["old_dl"], disc="mem_DL_0w2h2t")
    #of = open("old_dl_blr_opt.tex", "w")
    #of.write(r.print_tree_latex())
    #of.close()
    #of = open("old_dl_blr_opt.pickle", "w")
    #of.write(pickle.dumps(r))
    #of.close()

    #r = Categorize.CategorizationFromString(trees["old_2t_blr_A"])
    #r.axes = Categorize.Categorization.axes

    #r.eval_limit("old_2t_blr_A")

    #print "Old categorization"
    #make_latex("old")
    #make_latex("old_2t")

    #make_latex("old")
    #make_latex("old_2t_blr_A")


#    r = split_leaves_by_BLR(trees["old_2t"])
#    of = open("old_2t_blr_opt.tex", "w")
#    print r.print_tree()
#    of.write(r.print_tree_latex())
#    of.close()
#    of = open("old_2t_blr_opt.pickle", "w")
#    of.write(pickle.dumps(r))
#    of.close()
    

    #make_latex("old")

    #r = split_leaves_by_BLR_highpurity(trees["old_blr"])
    #of = open("old_blr_highpurity_opt.tex", "w")
    #print r.print_tree()
    #of.write(r.print_tree_latex())
    #of.close()
    #of = open("old_blr_highpurity_opt.pickle", "w")
    #of.write(pickle.dumps(r))
    #of.close()


    #print "Optimization"
    #r = Categorize.CategorizationFromString(trees["3cat"])
    #name = "opt"

    #import cProfile, time
    #def f(): optimize(r)
    #p = cProfile.Profile(time.clock)
    #p.runcall(f)
    #p.print_stats()
    #
    #of = open( name + ".tex","w")
    #of.write(r.print_tree_latex())
    #of.close()
    #of = open(name + ".pickle", "w")
    #of.write(pickle.dumps(r))
    #of.close()


    #for i in range(5,7):
    #    make_latex("{0}cat".format(i))
    #    r = Categorize.CategorizationFromString(trees["{0}cat".format(i)])
    #    print r.eval_limit("{0}cat".format(i))
        
