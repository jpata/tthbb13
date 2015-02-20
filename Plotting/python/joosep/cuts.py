import ROOT, sys, glob

#use only nominal systematic
cut_nom = "(syst == 0)"

#from mem_categories
cut_cat1   = cut_nom + "&&" + "(( type==0 || (type==3 && flag_type3>0))   && btag_LR>=0.)"
cut_cat2   = cut_nom + "&&" + "(( type==1 || (type==3 && flag_type3<=0) ) && btag_LR>=0.)"
cut_cat3   = cut_nom + "&&" + "(type==2 && flag_type2<=999 && btag_LR>=0.)"
cut_cat6   = cut_nom + "&&" + "(type==6 && btag_LR>=0.)"

cut_cat1_H = cut_nom + "&&" + "(( type==0 || (type==3 && flag_type3>0)) && btag_LR>=0.995)"
cut_cat1_L = cut_nom + "&&" + "(( type==0 || (type==3 && flag_type3>0)) && btag_LR<0.995 && btag_LR>=0.960)"

cut_cat2_H = cut_nom + "&&" + "(( type==1 || (type==3 && flag_type3<=0) ) && btag_LR>=0.9925)"
cut_cat2_L = cut_nom + "&&" + "(( type==1 || (type==3 && flag_type3<=0) ) && btag_LR<0.9925 && btag_LR>=0.960)"

cut_cat3_H = cut_nom + "&&" + "(type==2 && flag_type2<=999 && btag_LR>=0.995)"
cut_cat3_L = cut_nom + "&&" + "(type==2 && flag_type2<=999 && btag_LR<0.995 && btag_LR>=0.970)"

cut_cat6_H = cut_nom + "&&" + "(type==6 && btag_LR>=0.925)"
cut_cat6_L = cut_nom + "&&" + "(type==6 && btag_LR<0.925 && btag_LR>=0.850)";

cut_CSVL_4 = cut_nom + "&&" + "(numBTagL == 4)"
cut_CSVM_4 = cut_nom + "&&" + "(numBTagM == 4)"
cut_CSVT_4 = cut_nom + "&&" + "(numBTagT == 4)"

#jet multiplicities
cut_bb = "( nMatchSimBs>=2 && nMatchSimCs<=0 )"
cut_bj = "( nMatchSimBs==1 && nMatchSimCs<=0)"
cut_cc = "( nMatchSimBs==0 && nMatchSimCs>=1 )"
cut_jj = "( nMatchSimBs==0 && nMatchSimCs==0 )"

def get_sync_table(sample):
    ch = ROOT.TChain("tree")
    for f in sample.fileNamesS2:
        ch.AddFile(f)
    print "total", ch.GetEntries(), ch.GetEntries(cut_nom)

    cats = [
        ("cat1", cut_cat1, cut_cat1_L, cut_cat1_H),
        ("cat2", cut_cat2, cut_cat2_L, cut_cat2_H),
        ("cat3", cut_cat3, cut_cat3_L, cut_cat3_H),
        ("cat6", cut_cat6, cut_cat6_L, cut_cat6_H),
        ("ntag", cut_CSVL_4, cut_CSVM_4, cut_CSVT_4),
    ]
    nick = sample.nickName.value()
    if "8TeV" in nick:
        cats += [("lep", "", cut_nom+"&&"+"(Vtype==3 || Vtype==2)", cut_nom+"&&"+"(Vtype==4 || Vtype==0 || Vtype==1)")]
    if "13TeV" in nick:
        cats += [("lep", "", cut_nom+"&&"+"(Vtype==3 || Vtype==2)", cut_nom+"&&"+"(Vtype==5 || Vtype==0 || Vtype==1)")]

    for catname, tot, l, h in cats:
        print catname, ch.GetEntries(tot), ch.GetEntries(l), ch.GetEntries(h)

if __name__ == "__main__":
    from TTH.Plotting.joosep.samples import samples
    for sample in samples:
        print sample.nickName.value()
        get_sync_table(sample)
