import FWCore.ParameterSet.Config as cms

# Z->ll veto
ADDZLLVETO    = 1

# used to be 1
ADDPIXELVETO  = 0

# for higgs jets (not needed)
ADDDIJETPTCUT = 0

# require N jets above 40
ADDJETPT40CUT = 0

# min nr jets with pt>40 
NR_PT40_JETS  = 4


##########################################
##########################################

## -1 ==> data_obs = bkg + sgn
##  0 ==> data_obs = bkg
## +1 ==> data_obs = Run2012

RUNONDATA      = 1
extraNameBlind = ""
if RUNONDATA==0:
    extraNameBlind = "_MC"
if RUNONDATA<0:
    extraNameBlind = "_MC-sb"

###########################################
###########################################

# baseline
cat = cms.PSet(
    
    name      = cms.string("New"),
    version   = cms.string("_rec_std"),
    extraname = cms.string(""),
    fname     = cms.string("MEM"),
    inputpath = cms.string("../root/files/byLLR/Apr23_2014/"),
    directory = cms.string("PreApproval/checks"),
    cut       = cms.string(""),
    category  = cms.string(""),
    varname   = cms.string(""),
    doMEM     = cms.int32(4),
    fact1     = cms.double(0),
    fact2     = cms.double(0),
    factbb    = cms.double(0),
    lumiScale = cms.double(19.51/12.1), #19.04
    nBins     = cms.int32(6),
    nBinsY    = cms.untracked.int32(1),
    splitFirstBin = cms.int32(0),
    binvec        = cms.vdouble(),
    binvecY       = cms.vdouble(),
    samples       = cms.vstring( "TTV", "SingleT", "DiBoson", "TTJetsBB",
                                 "TTJetsBJ", "TTJetsCC", "TTJetsJJ", "TTH125", "EWK",
                                 "Run2012_SingleMu", "Run2012_SingleElectron"),
    nparts= cms.int32(1),
    part  = cms.int32(0),

    # 0 = SL, 1 = DL
    analysis      = cms.untracked.int32(-1),
    doSystematics = cms.untracked.int32(1),
    runOnData     = cms.untracked.int32(RUNONDATA),
    massH         = cms.untracked.double(125.),
    do2Dplots     = cms.untracked.int32(0)

    )

################### category cut

cut_cat1   = "( type==0 || (type==3 && flag_type3>0))   && btag_LR>=0."
cut_cat2   = "( type==1 || (type==3 && flag_type3<=0) ) && btag_LR>=0."
cut_cat3   = "type==2 && flag_type2<=999 && btag_LR>=0."
cut_cat6   = "type==6 && btag_LR>=0."

cut_cat1_H = "( type==0 || (type==3 && flag_type3>0)) && btag_LR>=0.995"
cut_cat1_L = "( type==0 || (type==3 && flag_type3>0)) && btag_LR<0.995 && btag_LR>=0.960"

cut_cat2_H = "( type==1 || (type==3 && flag_type3<=0) ) && btag_LR>=0.9925"
cut_cat2_L = "( type==1 || (type==3 && flag_type3<=0) ) && btag_LR<0.9925 && btag_LR>=0.960"

cut_cat3_H = "type==2 && flag_type2<=999 && btag_LR>=0.995"
cut_cat3_L = "type==2 && flag_type2<=999 && btag_LR<0.995 && btag_LR>=0.970"

cut_cat6_H = "type==6 && btag_LR>=0.925"
cut_cat6_L = "type==6 && btag_LR<0.925 && btag_LR>=0.850"

#################### category variable

var_cat1_H = "p_125_all_s_ttbb/(p_125_all_s_ttbb+1.200000*(0.005916*p_125_all_b_ttbb+85.645287*p_125_all_b_ttjj))"
var_cat1_L = "p_125_all_s_ttbb/(p_125_all_s_ttbb+1.200000*(0.006597*p_125_all_b_ttbb+3.056202*p_125_all_b_ttjj))"
var_cat2_H = "p_125_all_s_ttbb/(p_125_all_s_ttbb+0.600000*(0.013812*p_125_all_b_ttbb+68.346115*p_125_all_b_ttjj))"
var_cat2_L = "p_125_all_s_ttbb/(p_125_all_s_ttbb+1.800000*(0.003168*p_125_all_b_ttbb+1.346579*p_125_all_b_ttjj))"
var_cat3_H = "p_125_all_s_ttbb/(p_125_all_s_ttbb+0.600000*(0.012640*p_125_all_b_ttbb+64.279221*p_125_all_b_ttjj))"
var_cat3_L = "p_125_all_s_ttbb/(p_125_all_s_ttbb+2.000000*(0.001554*p_125_all_b_ttbb+1.565640*p_125_all_b_ttjj))"
var_cat6_H = "p_125_all_s_ttbb/(p_125_all_s_ttbb+0.600000*(0.014056*p_125_all_b_ttbb+6.107426*p_125_all_b_ttjj))"
var_cat6_L = "p_125_all_s_ttbb/(p_125_all_s_ttbb+2.000000*(0.001497*p_125_all_b_ttbb+0.018406*p_125_all_b_ttjj))"

#################### ttbb vs ttjj discrimination

cat1_bj = cat.clone(
    extraname = cms.string("_bj"+extraNameBlind),
    cut       = cms.string(cut_cat1), #0.975
    category  = cms.string("cat1"),
    doMEM     = cms.int32(3),
    factbb    = cms.double(0.15)
    )

cat2_bj = cat.clone(
    extraname = cms.string("_bj"+extraNameBlind),
    cut       = cms.string(cut_cat2),#0.975
    category  = cms.string("cat2"),
    doMEM     = cms.int32(3),
    factbb    = cms.double(0.20)
    )

cat3_bj = cat.clone(
    extraname = cms.string("_bj"+extraNameBlind),
    cut       = cms.string(cut_cat3), #0.990
    category  = cms.string("cat3"),
    doMEM     = cms.int32(3),
    factbb    = cms.double(0.50)
    )

cat6_bj = cat.clone(
    extraname = cms.string("_bj"+extraNameBlind),
    cut       = cms.string(cut_cat6),#0.980
    category  = cms.string("cat6"),
    factbb    = cms.double(0.15),
    doMEM     = cms.int32(3),
    samples   = cms.vstring( "TTV", "SingleT", "DiBoson", "TTJetsBB",
                             "TTJetsBJ", "TTJetsCC", "TTJetsJJ", "TTH125", "EWK",
                             "Run2012_SingleMu", "Run2012_DoubleElectron")
    ) 

#################### ttbb vs ttH separation (no bias)

cat1_sb_nb =  cat1_bj.clone(
    cut       = cms.string(cut_cat1_H),
    extraname     = cms.string("_sb_nb"+extraNameBlind),
    doMEM         = cms.int32(-2),
    fact1         = cms.double(1.2),
    splitFirstBin = cms.int32(1),
    )

cat2_sb_nb =  cat2_bj.clone(
    cut       = cms.string(cut_cat2_H),
    extraname = cms.string("_sb_nb"+extraNameBlind),
    doMEM     = cms.int32(-2),
    fact1     = cms.double(0.6),
    splitFirstBin = cms.int32(1),
    )

cat3_sb_nb =  cat3_bj.clone(
    cut       = cms.string(cut_cat3_H),
    extraname = cms.string("_sb_nb"+extraNameBlind),   
    doMEM     = cms.int32(-2),
    fact1     = cms.double(0.6),
    splitFirstBin = cms.int32(1),   
    )

cat6_sb_nb =  cat6_bj.clone(
    cut       = cms.string(cut_cat6_H),
    extraname = cms.string("_sb_nb"+extraNameBlind),
    doMEM     = cms.int32(-2),
    fact1     = cms.double(0.6),
    splitFirstBin = cms.int32(1),    
    )


#################### ttbb vs ttH separation

cat1_sb =  cat1_sb_nb.clone(
    cut       = cms.string( cut_cat1 ),
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    )

cat2_sb =  cat2_sb_nb.clone(
    cut       = cms.string( cut_cat2 ),
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    )

cat3_sb =  cat3_sb_nb.clone(
    cut       = cms.string( cut_cat3 ),
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    )

cat6_sb =  cat6_sb_nb.clone(
    cut       = cms.string( cut_cat6 ), 
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    )

#################### ttbb vs ttH separation (no bias) !!! new !!!

cat1_sb_H =  cat1_bj.clone(
    cut           = cms.string(cut_cat1_H),
    category      = cms.string("cat1_H"),
    extraname     = cms.string("_sb"+extraNameBlind),
    doMEM         = cms.int32(2),
    fact1         = cms.double(1.2),
    splitFirstBin = cms.int32(1),
    )


cat1_sb_L =  cat1_bj.clone(
    cut           = cms.string(cut_cat1_L),
    category      = cms.string("cat1_L"),
    extraname     = cms.string("_sb"+extraNameBlind),
    doMEM         = cms.int32(2),
    fact1         = cms.double(1.2),
    splitFirstBin = cms.int32(0),
    )


cat2_sb_H =  cat2_bj.clone(
    cut       = cms.string(cut_cat2_H),
    category  = cms.string("cat2_H"), 
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    fact1     = cms.double(0.6),
    splitFirstBin = cms.int32(1),
    )

cat2_sb_L =  cat2_bj.clone(
    cut       = cms.string(cut_cat2_L),
    category  = cms.string("cat2_L"), 
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    fact1     = cms.double(1.8),
    splitFirstBin = cms.int32(0),
    )


cat3_sb_H =  cat3_bj.clone(
    cut       = cms.string(cut_cat3_H), 
    category  = cms.string("cat3_H"), 
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    fact1     = cms.double(0.6),
    splitFirstBin = cms.int32(1),   
    )

cat3_sb_L =  cat3_bj.clone(
    cut       = cms.string(cut_cat3_L), 
    category  = cms.string("cat3_L"), 
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    fact1     = cms.double(2.0),
    splitFirstBin = cms.int32(0),   
    )

cat6_sb_H =  cat6_bj.clone(
    cut       = cms.string(cut_cat6_H),
    category  = cms.string("cat6_H"), 
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    fact1     = cms.double(0.6),
    splitFirstBin = cms.int32(1),
    nBins     = cms.int32(6),
    )

cat6_sb_L =  cat6_bj.clone(
    cut       = cms.string(cut_cat6_L),
    category  = cms.string("cat6_L"), 
    extraname = cms.string("_sb"+extraNameBlind),
    doMEM     = cms.int32(2),
    fact1     = cms.double(2.0),
    splitFirstBin = cms.int32(0),
    nBins     = cms.int32(6),
    )
