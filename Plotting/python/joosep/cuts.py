
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

#jet multiplicities
cut_bb = "( nMatchSimBs>=2 && nMatchSimCs<=0 )"
cut_bj = "( nMatchSimBs==1 && nMatchSimCs<=0)"
cut_cc = "( nMatchSimBs==0 && nMatchSimCs>=1 )"
cut_jj = "( nMatchSimBs==0 && nMatchSimCs==0 )"
