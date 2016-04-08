
trees = {}

# Classic categorization:
# Based on jet and tagged jet multiplicity
# 7 categories

trees["6j_ge3t"] = """
  Discr=counting
     eventParity__0__1 Discr=None
     eventParity__1__2 Discr=counting
        numJets__4__5 Discr=None
        numJets__5__8 Discr=counting
           numJets__5__6 Discr=None
           numJets__6__8 Discr=counting
              nBCSVM__1__3 Discr=None
              nBCSVM__3__8 Discr=counting
"""

trees["6j_ge3t_test1"] = """
  Discr=counting
     eventParity__0__1 Discr=None
     eventParity__1__2 Discr=counting
        numJets__4__5 Discr=None
        numJets__5__8 Discr=counting
           numJets__5__6 Discr=None
           numJets__6__8 Discr=counting
              nBCSVM__1__3 Discr=None
              nBCSVM__3__8 Discr=counting
                 mem_SL_0w2h2t__0_0__0_444444444444 Discr=counting
                    mem_SL_0w2h2t__0_0__0_222222222222 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                       btag_LR_4b_2b_logit__7_2__20_0 Discr=counting
                    mem_SL_0w2h2t__0_222222222222__0_444444444444 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
                       btag_LR_4b_2b_logit__6_4__20_0 Discr=counting
                 mem_SL_0w2h2t__0_444444444444__1_0 Discr=counting
                    mem_SL_0w2h2t__0_444444444444__0_722222222222 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__5_6 Discr=counting
                       btag_LR_4b_2b_logit__5_6__20_0 Discr=counting
                    mem_SL_0w2h2t__0_722222222222__1_0 Discr=counting
"""

trees["6j_ge3t_test2"] = """
  Discr=counting
     eventParity__0__1 Discr=counting
        numJets__3__5 Discr=None
        numJets__5__7 Discr=counting
           numJets__5__6 Discr=None
           numJets__6__7 Discr=counting
              nBCSVM__1__3 Discr=None
              nBCSVM__3__5 Discr=counting
                 mem_SL_0w2h2t__0_0__0_444444444444 Discr=counting
                    mem_SL_0w2h2t__0_0__0_222222222222 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                          mem_SL_0w2h2t__0_0__0_166666666667 Discr=counting
                             btag_LR_4b_2b_logit__m20_0__4_0 Discr=counting
                                btag_LR_4b_2b_logit__m20_0__2_4 Discr=counting
                                   btag_LR_4b_2b_logit__m20_0__1_6 Discr=counting
                                   btag_LR_4b_2b_logit__1_6__2_4 Discr=counting
                                btag_LR_4b_2b_logit__2_4__4_0 Discr=counting
                                   btag_LR_4b_2b_logit__2_4__3_2 Discr=counting
                                   btag_LR_4b_2b_logit__3_2__4_0 Discr=counting
                             btag_LR_4b_2b_logit__4_0__7_2 Discr=counting
                                mem_SL_0w2h2t__0_0__0_0555555555556 Discr=counting
                                   btag_LR_4b_2b_logit__4_0__5_6 Discr=counting
                                      btag_LR_4b_2b_logit__4_0__4_8 Discr=counting
                                      btag_LR_4b_2b_logit__4_8__5_6 Discr=counting
                                   btag_LR_4b_2b_logit__5_6__7_2 Discr=counting
                                mem_SL_0w2h2t__0_0555555555556__0_166666666667 Discr=counting
                                   mem_SL_0w2h2t__0_0555555555556__0_111111111111 Discr=counting
                                   mem_SL_0w2h2t__0_111111111111__0_166666666667 Discr=counting
                          mem_SL_0w2h2t__0_166666666667__0_222222222222 Discr=counting
                       btag_LR_4b_2b_logit__7_2__20_0 Discr=counting
                    mem_SL_0w2h2t__0_222222222222__0_444444444444 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
                          mem_SL_0w2h2t__0_222222222222__0_333333333333 Discr=counting
                             btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                             btag_LR_4b_2b_logit__4_8__6_4 Discr=counting
                          mem_SL_0w2h2t__0_333333333333__0_444444444444 Discr=counting
                             btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                             btag_LR_4b_2b_logit__4_8__6_4 Discr=counting
                       btag_LR_4b_2b_logit__6_4__20_0 Discr=counting
                 mem_SL_0w2h2t__0_444444444444__1_0 Discr=counting
                    mem_SL_0w2h2t__0_444444444444__0_722222222222 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__5_6 Discr=counting
                          btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                             mem_SL_0w2h2t__0_444444444444__0_638888888889 Discr=counting
                                mem_SL_0w2h2t__0_444444444444__0_555555555556 Discr=counting
                                mem_SL_0w2h2t__0_555555555556__0_638888888889 Discr=counting
                             mem_SL_0w2h2t__0_638888888889__0_722222222222 Discr=counting
                          btag_LR_4b_2b_logit__4_8__5_6 Discr=counting
                       btag_LR_4b_2b_logit__5_6__20_0 Discr=counting
                          mem_SL_0w2h2t__0_444444444444__0_611111111111 Discr=counting
                          mem_SL_0w2h2t__0_611111111111__0_722222222222 Discr=counting
                    mem_SL_0w2h2t__0_722222222222__1_0 Discr=counting
     eventParity__1__2 Discr=counting
        numJets__3__5 Discr=None
        numJets__5__7 Discr=counting
           numJets__5__6 Discr=None
           numJets__6__7 Discr=counting
              nBCSVM__1__3 Discr=None
              nBCSVM__3__5 Discr=counting
                 mem_SL_0w2h2t__0_0__0_444444444444 Discr=counting
                    mem_SL_0w2h2t__0_0__0_222222222222 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                          mem_SL_0w2h2t__0_0__0_166666666667 Discr=counting
                             btag_LR_4b_2b_logit__m20_0__4_0 Discr=counting
                                btag_LR_4b_2b_logit__m20_0__2_4 Discr=counting
                                   btag_LR_4b_2b_logit__m20_0__1_6 Discr=counting
                                   btag_LR_4b_2b_logit__1_6__2_4 Discr=counting
                                btag_LR_4b_2b_logit__2_4__4_0 Discr=counting
                                   btag_LR_4b_2b_logit__2_4__3_2 Discr=counting
                                   btag_LR_4b_2b_logit__3_2__4_0 Discr=counting
                             btag_LR_4b_2b_logit__4_0__7_2 Discr=counting
                                mem_SL_0w2h2t__0_0__0_0555555555556 Discr=counting
                                   btag_LR_4b_2b_logit__4_0__5_6 Discr=counting
                                      btag_LR_4b_2b_logit__4_0__4_8 Discr=counting
                                      btag_LR_4b_2b_logit__4_8__5_6 Discr=counting
                                   btag_LR_4b_2b_logit__5_6__7_2 Discr=counting
                                mem_SL_0w2h2t__0_0555555555556__0_166666666667 Discr=counting
                                   mem_SL_0w2h2t__0_0555555555556__0_111111111111 Discr=counting
                                   mem_SL_0w2h2t__0_111111111111__0_166666666667 Discr=counting
                          mem_SL_0w2h2t__0_166666666667__0_222222222222 Discr=counting
                       btag_LR_4b_2b_logit__7_2__20_0 Discr=counting
                    mem_SL_0w2h2t__0_222222222222__0_444444444444 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
                          mem_SL_0w2h2t__0_222222222222__0_333333333333 Discr=counting
                             btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                             btag_LR_4b_2b_logit__4_8__6_4 Discr=counting
                          mem_SL_0w2h2t__0_333333333333__0_444444444444 Discr=counting
                             btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                             btag_LR_4b_2b_logit__4_8__6_4 Discr=counting
                       btag_LR_4b_2b_logit__6_4__20_0 Discr=counting
                 mem_SL_0w2h2t__0_444444444444__1_0 Discr=counting
                    mem_SL_0w2h2t__0_444444444444__0_722222222222 Discr=counting
                       btag_LR_4b_2b_logit__m20_0__5_6 Discr=counting
                          btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                             mem_SL_0w2h2t__0_444444444444__0_638888888889 Discr=counting
                                mem_SL_0w2h2t__0_444444444444__0_555555555556 Discr=counting
                                mem_SL_0w2h2t__0_555555555556__0_638888888889 Discr=counting
                             mem_SL_0w2h2t__0_638888888889__0_722222222222 Discr=counting
                          btag_LR_4b_2b_logit__4_8__5_6 Discr=counting
                       btag_LR_4b_2b_logit__5_6__20_0 Discr=counting
                          mem_SL_0w2h2t__0_444444444444__0_611111111111 Discr=counting
                          mem_SL_0w2h2t__0_611111111111__0_722222222222 Discr=counting
                    mem_SL_0w2h2t__0_722222222222__1_0 Discr=counting
""" 



trees["old"] = """
  Discr=mem_SL_0w2h2t
     numJets__4__5 Discr=mem_SL_0w2h2t 
        nBCSVM__2__4 Discr=mem_SL_0w2h2t
           nBCSVM__2__3 Discr=None
           nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
        nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
     numJets__5__8 Discr=mem_SL_0w2h2t
        numJets__5__6 Discr=mem_SL_0w2h2t
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
        numJets__6__8 Discr=mem_SL_0w2h2t
           nBCSVM__1__4 Discr=mem_SL_0w2h2t
              nBCSVM__1__3 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__1__2 Discr=None
                 nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
           nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
"""

trees["old_mem_bdt2d_stratB"] = """
  Discr=mem_SL_0w2h2t
     eventParity__0__1 Discr=mem_SL_0w2h2t 
        numJets__4__5 Discr=mem_SL_0w2h2t 
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
                 common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
        numJets__5__8 Discr=mem_SL_0w2h2t 
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__2__4 Discr=mem_SL_0w2h2t
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_15 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_15__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
           numJets__6__8 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=common_bdt rebin=2
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=6
     eventParity__1__2 Discr=counting
        numJets__4__5 Discr=mem_SL_0w2h2t 
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
        numJets__5__8 Discr=mem_SL_0w2h2t 
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__2__4 Discr=mem_SL_0w2h2t
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_15 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_15__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
           numJets__6__8 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=common_bdt rebin=2
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=6
"""


trees["old_mem_bdt2d"] = """
  Discr=mem_SL_0w2h2t
     eventParity__0__1 Discr=mem_SL_0w2h2t 
        numJets__4__5 Discr=mem_SL_0w2h2t 
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
        numJets__5__8 Discr=mem_SL_0w2h2t 
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__2__4 Discr=mem_SL_0w2h2t
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_15 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_15__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
           numJets__6__8 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=4
                       common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=4
                       common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=6
     eventParity__1__2 Discr=counting
        numJets__4__5 Discr=mem_SL_0w2h2t 
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
        numJets__5__8 Discr=mem_SL_0w2h2t 
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__2__4 Discr=mem_SL_0w2h2t
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_15 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_15__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
           numJets__6__8 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=4
                       common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=4
                       common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=6
"""

trees["old_mem_bdt2d_unsplit"] = """
  Discr=mem_SL_0w2h2t
     numJets__4__5 Discr=mem_SL_0w2h2t 
        nBCSVM__2__4 Discr=mem_SL_0w2h2t
           nBCSVM__2__3 Discr=None
           nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
              common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=4
              common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
        nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
           common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
           common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
     numJets__5__8 Discr=mem_SL_0w2h2t 
        numJets__5__6 Discr=mem_SL_0w2h2t
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__m1_0__0_15 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__0_15__1_0 Discr=mem_SL_0w2h2t rebin=4
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__m1_0__0_2 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
        numJets__6__8 Discr=mem_SL_0w2h2t
           nBCSVM__1__4 Discr=mem_SL_0w2h2t
              nBCSVM__1__3 Discr=mem_SL_0w2h2t
                 nBCSVM__1__2 Discr=None
                 nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
           nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__m1_0__0_1 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=6
"""

trees["old_mem_bdt2d_v2"] = """
  Discr=mem_SL_0w2h2t
     eventParity__0__1 Discr=mem_SL_0w2h2t 
        numJets__4__5 Discr=mem_SL_0w2h2t 
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__m1_0__0_2 Discr=common_bdt rebin=2
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__m1_0__0_2 Discr=common_bdt rebin=4
              common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
        numJets__5__8 Discr=mem_SL_0w2h2t 
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__2__4 Discr=mem_SL_0w2h2t
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_2 Discr=common_bdt rebin=2
                    common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_2 Discr=common_bdt rebin=4
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
           numJets__6__8 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=4
                       common_bdt__m1_0__0_1 Discr=common_bdt rebin=2
                       common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_1 Discr=common_bdt rebin=2
                    common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_0 Discr=common_bdt rebin=4
                 common_bdt__0_0__1_0 Discr=mem_SL_0w2h2t rebin=6
     eventParity__1__2 Discr=counting
        numJets__4__5 Discr=mem_SL_0w2h2t
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                 common_bdt__m1_0__0_2 Discr=common_bdt rebin=2
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
              common_bdt__m1_0__0_2 Discr=common_bdt rebin=4
              common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
        numJets__5__8 Discr=mem_SL_0w2h2t 
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__2__4 Discr=mem_SL_0w2h2t
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_2 Discr=common_bdt rebin=2
                    common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_2 Discr=common_bdt rebin=4
                 common_bdt__0_2__1_0 Discr=mem_SL_0w2h2t rebin=6
           numJets__6__8 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=4
                       common_bdt__m1_0__0_1 Discr=common_bdt rebin=2
                       common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=4
                    common_bdt__m1_0__0_1 Discr=common_bdt rebin=2
                    common_bdt__0_1__1_0 Discr=mem_SL_0w2h2t rebin=4
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
                 common_bdt__m1_0__0_0 Discr=common_bdt rebin=4
                 common_bdt__0_0__1_0 Discr=mem_SL_0w2h2t rebin=6
"""

trees["old_rebin"] = """
  Discr=mem_SL_0w2h2t
     numJets__4__5 Discr=mem_SL_0w2h2t 
        nBCSVM__2__4 Discr=mem_SL_0w2h2t
           nBCSVM__2__3 Discr=None
           nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
        nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=4
     numJets__5__8 Discr=mem_SL_0w2h2t
        numJets__5__6 Discr=mem_SL_0w2h2t
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=4
        numJets__6__8 Discr=mem_SL_0w2h2t
           nBCSVM__1__4 Discr=mem_SL_0w2h2t
              nBCSVM__1__3 Discr=mem_SL_0w2h2t
                 nBCSVM__1__2 Discr=None
                 nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=2
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
           nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
"""

trees["old_rebin_parity"] = """
  Discr=mem_SL_0w2h2t
     eventParity__0__1 Discr=mem_SL_0w2h2t
        numJets__4__5 Discr=mem_SL_0w2h2t 
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=4
        numJets__5__8 Discr=mem_SL_0w2h2t
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__2__4 Discr=mem_SL_0w2h2t
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=4
           numJets__6__8 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=2
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6       
     eventParity__1__2 Discr=mem_SL_0w2h2t
        numJets__4__5 Discr=mem_SL_0w2h2t 
           nBCSVM__2__4 Discr=mem_SL_0w2h2t
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=4
        numJets__5__8 Discr=mem_SL_0w2h2t
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__2__4 Discr=mem_SL_0w2h2t
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=4
           numJets__6__8 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=2
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=2
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6       
"""

trees["old_rebin_bdt_parity"] = """
  Discr=common_bdt
     eventParity__0__1 Discr=common_bdt
        numJets__4__5 Discr=common_bdt 
           nBCSVM__2__4 Discr=common_bdt
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=common_bdt rebin=2
           nBCSVM__4__5 Discr=common_bdt rebin=4
        numJets__5__8 Discr=common_bdt
           numJets__5__6 Discr=common_bdt
              nBCSVM__2__4 Discr=common_bdt
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=common_bdt rebin=2
              nBCSVM__4__5 Discr=common_bdt rebin=4
           numJets__6__8 Discr=common_bdt
              nBCSVM__1__4 Discr=common_bdt
                 nBCSVM__1__3 Discr=common_bdt
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=common_bdt rebin=2
                 nBCSVM__3__4 Discr=common_bdt rebin=2
              nBCSVM__4__8 Discr=common_bdt rebin=5
     eventParity__1__2 Discr=common_bdt
        numJets__4__5 Discr=common_bdt 
           nBCSVM__2__4 Discr=common_bdt
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=common_bdt rebin=2
           nBCSVM__4__5 Discr=common_bdt rebin=4
        numJets__5__8 Discr=common_bdt
           numJets__5__6 Discr=common_bdt
              nBCSVM__2__4 Discr=common_bdt
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=common_bdt rebin=2
              nBCSVM__4__5 Discr=common_bdt rebin=4
           numJets__6__8 Discr=common_bdt
              nBCSVM__1__4 Discr=common_bdt
                 nBCSVM__1__3 Discr=common_bdt
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=common_bdt rebin=2
                 nBCSVM__3__4 Discr=common_bdt rebin=2
              nBCSVM__4__8 Discr=common_bdt rebin=5
"""


trees["old_parity"] = """
  Discr=mem_SL_0w2h2t rebin=6
     eventParity__0__1 Discr=mem_SL_0w2h2t rebin=6
        numJets__4__5 Discr=mem_SL_0w2h2t rebin=6 
           nBCSVM__2__4 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__2__3 Discr=None rebin=6
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
        numJets__5__8 Discr=mem_SL_0w2h2t rebin=6
           numJets__5__6 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__2__4 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
           numJets__6__8 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__1__4 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t rebin=6
                    nBCSVM__1__2 Discr=None rebin=6
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
     eventParity__1__2 Discr=mem_SL_0w2h2t rebin=6
        numJets__4__5 Discr=mem_SL_0w2h2t rebin=6
           nBCSVM__2__4 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__2__3 Discr=None rebin=6
              nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
           nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
        numJets__5__8 Discr=mem_SL_0w2h2t rebin=6
           numJets__5__6 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__2__4 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__2__3 Discr=None rebin=6
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
           numJets__6__8 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__1__4 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t rebin=6
                    nBCSVM__1__2 Discr=None rebin=6
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6
"""

# Result of running leaf optimization using BLR and counting on 7 category old tree
trees["old_blrsplit"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__1_6 Discr=mem_SL_0w2h2t rebin=6
             btag_LR_4b_2b_logit__1_6__20_0 Discr=mem_SL_0w2h2t rebin=6
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t rebin=6
          btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t rebin=6
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__3_2 Discr=mem_SL_0w2h2t rebin=6
                btag_LR_4b_2b_logit__3_2__20_0 Discr=mem_SL_0w2h2t rebin=6
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t rebin=6
             btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t rebin=6
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
                   btag_LR_4b_2b_logit__m20_0__0_0 Discr=counting rebin=6
                   btag_LR_4b_2b_logit__0_0__20_0 Discr=mem_SL_0w2h2t rebin=6
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_0 Discr=mem_SL_0w2h2t rebin=6
                btag_LR_4b_2b_logit__4_0__20_0 Discr=mem_SL_0w2h2t rebin=6
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t rebin=6
             btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t rebin=6
"""

# Result of running leaf optimization using BLR and counting on 7 category old tree
trees["old_blrsplit_mem_bdt_parity"] = """
  Discr=mem_SL_0w2h2t
     eventParity__0__1 Discr=mem_SL_0w2h2t
        numJets__3__5 Discr=mem_SL_0w2h2t
           nBCSVM__1__4 Discr=mem_SL_0w2h2t
              nBCSVM__1__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__m20_0__1_6 Discr=common_bdt
                 btag_LR_4b_2b_logit__1_6__20_0 Discr=mem_SL_0w2h2t
           nBCSVM__4__5 Discr=mem_SL_0w2h2t
              btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
              btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
        numJets__5__7 Discr=mem_SL_0w2h2t
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t
                    btag_LR_4b_2b_logit__m20_0__3_2 Discr=common_bdt
                    btag_LR_4b_2b_logit__3_2__20_0 Discr=mem_SL_0w2h2t
              nBCSVM__4__5 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
           numJets__6__7 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t
                       btag_LR_4b_2b_logit__m20_0__0_0 Discr=common_bdt
                       btag_LR_4b_2b_logit__0_0__20_0 Discr=common_bdt
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t
                    btag_LR_4b_2b_logit__m20_0__4_0 Discr=common_bdt
                    btag_LR_4b_2b_logit__4_0__20_0 Discr=mem_SL_0w2h2t
              nBCSVM__4__5 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
     eventParity__1__2 Discr=mem_SL_0w2h2t
        numJets__3__5 Discr=mem_SL_0w2h2t
           nBCSVM__1__4 Discr=mem_SL_0w2h2t
              nBCSVM__1__3 Discr=None
              nBCSVM__3__4 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__m20_0__1_6 Discr=common_bdt
                 btag_LR_4b_2b_logit__1_6__20_0 Discr=mem_SL_0w2h2t
           nBCSVM__4__5 Discr=mem_SL_0w2h2t
              btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
              btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
        numJets__5__7 Discr=mem_SL_0w2h2t
           numJets__5__6 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=None
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t
                    btag_LR_4b_2b_logit__m20_0__3_2 Discr=common_bdt
                    btag_LR_4b_2b_logit__3_2__20_0 Discr=mem_SL_0w2h2t
              nBCSVM__4__5 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
           numJets__6__7 Discr=mem_SL_0w2h2t
              nBCSVM__1__4 Discr=mem_SL_0w2h2t
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t
                       btag_LR_4b_2b_logit__m20_0__0_0 Discr=common_bdt
                       btag_LR_4b_2b_logit__0_0__20_0 Discr=mem_SL_0w2h2t
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t
                    btag_LR_4b_2b_logit__m20_0__4_0 Discr=mem_SL_0w2h2t
                    btag_LR_4b_2b_logit__4_0__20_0 Discr=mem_SL_0w2h2t
              nBCSVM__4__5 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
                 btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
"""

# Removed the splitting of the 6j2b category - it was useless (0 Signal, 1 of 5k BG events)
trees["old_blrsplit_A"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__5_6 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__5_6__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__8_8 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__8_8__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__5_6 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__5_6__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
"""

# Set a few of the categories to use counting
trees["old_blrsplit_B"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
             btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__5_6 Discr=counting
                btag_LR_4b_2b_logit__5_6__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__8_8 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__8_8__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__5_6 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__5_6__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
"""

# Set a few of the categories to use counting
trees["old_blrsplit_B_bdt"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__7_2 Discr=common_bdt
             btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__5_6 Discr=common_bdt
                btag_LR_4b_2b_logit__5_6__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__8_8 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__8_8__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=common_bdt
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__5_6 Discr=common_bdt
                btag_LR_4b_2b_logit__5_6__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_bdtsplit_A"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_5 Discr=mem_SL_0w2h2t
             common_bdt__0_5__1_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
          common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__0_666666666667 Discr=mem_SL_0w2h2t
                common_bdt__0_666666666667__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_333333333333 Discr=mem_SL_0w2h2t
             common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__0_333333333333 Discr=mem_SL_0w2h2t
                common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
"""

trees["old_bdtsplit_B"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_5 Discr=common_bdt
             common_bdt__0_5__1_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          common_bdt__m1_0__0_166666666667 Discr=common_bdt
          common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__0_666666666667 Discr=common_bdt
                common_bdt__0_666666666667__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_333333333333 Discr=common_bdt
             common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=common_bdt
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__0_333333333333 Discr=common_bdt
                common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_166666666667 Discr=common_bdt
             common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
"""

trees["old_bdtsplit"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_5 Discr=mem_SL_0w2h2t
             common_bdt__0_5__1_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
          common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__0_666666666667 Discr=mem_SL_0w2h2t
                common_bdt__0_666666666667__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_333333333333 Discr=mem_SL_0w2h2t
             common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
                   common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
                   common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__0_333333333333 Discr=mem_SL_0w2h2t
                common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
"""

# Removed one nonsense splitting
trees["old_bdtsplit_A"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_5 Discr=mem_SL_0w2h2t
             common_bdt__0_5__1_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
          common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__0_666666666667 Discr=mem_SL_0w2h2t
                common_bdt__0_666666666667__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_333333333333 Discr=mem_SL_0w2h2t
             common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__0_333333333333 Discr=mem_SL_0w2h2t
                common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
"""



# Split each bin by quantiles
trees["old_bdtsplit_B"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=None
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__m0_166666666667 Discr=mem_SL_0w2h2t
                common_bdt__m0_166666666667__0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
                common_bdt__0_166666666667__0_333333333333 Discr=mem_SL_0w2h2t
                common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__m0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__m0_166666666667__0_166666666667 Discr=mem_SL_0w2h2t
          common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=None
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__m0_5 Discr=mem_SL_0w2h2t
                common_bdt__m0_5__1_0 Discr=mem_SL_0w2h2t
                   common_bdt__m0_5__0_333333333333 Discr=mem_SL_0w2h2t
                   common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__m0_166666666667 Discr=mem_SL_0w2h2t
                common_bdt__m0_166666666667__0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
                common_bdt__0_166666666667__0_333333333333 Discr=mem_SL_0w2h2t
                common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__m0_166666666667 Discr=mem_SL_0w2h2t
                common_bdt__m0_166666666667__1_0 Discr=mem_SL_0w2h2t
                   common_bdt__m0_166666666667__0_333333333333 Discr=mem_SL_0w2h2t
                   common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_0 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__m0_166666666667 Discr=mem_SL_0w2h2t
                common_bdt__m0_166666666667__0_0 Discr=mem_SL_0w2h2t
             common_bdt__0_0__1_0 Discr=mem_SL_0w2h2t
                common_bdt__0_0__0_166666666667 Discr=mem_SL_0w2h2t
                common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
"""

# Classic categorization:
# Based on jet and tagged jet multiplicity. Also include the 2tag bins.
# 7 categories + 2 categories (4j2t, 5j2t)
trees["old_2t"] = """
  Discr=mem_SL_0w2h2t 
    numJets__4__5 Discr=mem_SL_0w2h2t 
       nBCSVM__1__4 Discr=mem_SL_0w2h2t
          nBCSVM__1__3 Discr=mem_SL_0w2h2t
             nBCSVM__1__2 Discr=None
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
    numJets__5__8 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
       numJets__6__8 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=mem_SL_0w2h2t
             nBCSVM__1__3 Discr=mem_SL_0w2h2t
                nBCSVM__1__2 Discr=None
                nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__8 Discr=mem_SL_0w2h2t
"""


trees["old_bdt"] = """
  Discr=common_bdt 
     eventParity__0__1 Discr=mem_SL_0w2h2t rebin=6
        numJets__4__5 Discr=common_bdt rebin=4 
           nBCSVM__2__4 Discr=common_bdt rebin=4
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=common_bdt rebin=4
           nBCSVM__4__5 Discr=common_bdt rebin=4
        numJets__5__8 Discr=common_bdt rebin=4
           numJets__5__6 Discr=common_bdt rebin=4
              nBCSVM__2__4 Discr=common_bdt rebin=4
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=common_bdt rebin=4
              nBCSVM__4__5 Discr=common_bdt rebin=4
           numJets__6__8 Discr=common_bdt rebin=4
              nBCSVM__1__4 Discr=common_bdt rebin=4
                 nBCSVM__1__3 Discr=common_bdt rebin=4
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=common_bdt rebin=4
                 nBCSVM__3__4 Discr=common_bdt rebin=4
              nBCSVM__4__8 Discr=common_bdt rebin=4
     eventParity__1__2 Discr=mem_SL_0w2h2t rebin=4
        numJets__4__5 Discr=common_bdt rebin=4
           nBCSVM__2__4 Discr=common_bdt rebin=4
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=common_bdt rebin=4
           nBCSVM__4__5 Discr=common_bdt rebin=4
        numJets__5__8 Discr=common_bdt rebin=4
           numJets__5__6 Discr=common_bdt rebin=4
              nBCSVM__2__4 Discr=common_bdt rebin=4
                 nBCSVM__2__3 Discr=None
                 nBCSVM__3__4 Discr=common_bdt rebin=4
              nBCSVM__4__5 Discr=common_bdt rebin=4
           numJets__6__8 Discr=common_bdt rebin=4
              nBCSVM__1__4 Discr=common_bdt rebin=4
                 nBCSVM__1__3 Discr=common_bdt rebin=4
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=common_bdt rebin=4
                 nBCSVM__3__4 Discr=common_bdt rebin=4
              nBCSVM__4__8 Discr=common_bdt rebin=4
"""

trees["old_bdt_mem"] = """
  Discr=common_bdt 
     numJets__4__5 Discr=common_bdt 
        nBCSVM__2__4 Discr=common_bdt
           nBCSVM__2__3 Discr=None
           nBCSVM__3__4 Discr=common_bdt
        nBCSVM__4__5 Discr=mem_SL_0w2h2t
     numJets__5__8 Discr=common_bdt
        numJets__5__6 Discr=common_bdt
           nBCSVM__2__4 Discr=common_bdt
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=common_bdt
           nBCSVM__4__5 Discr=mem_SL_0w2h2t
        numJets__6__8 Discr=common_bdt
           nBCSVM__1__4 Discr=common_bdt
              nBCSVM__1__3 Discr=common_bdt
                 nBCSVM__1__2 Discr=None
                 nBCSVM__2__3 Discr=common_bdt
              nBCSVM__3__4 Discr=common_bdt
           nBCSVM__4__8 Discr=mem_SL_0w2h2t
"""

#8.8, 7.2
trees["old_bdt_mem_blrsplit"] = """
  Discr=common_bdt 
     numJets__4__5 Discr=common_bdt 
        nBCSVM__2__4 Discr=common_bdt
           nBCSVM__2__3 Discr=None
           nBCSVM__3__4 Discr=common_bdt
        nBCSVM__4__5 Discr=mem_SL_0w2h2t
           btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
           btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
     numJets__5__8 Discr=common_bdt
        numJets__5__6 Discr=common_bdt
           nBCSVM__2__4 Discr=common_bdt
              nBCSVM__2__3 Discr=None
              nBCSVM__3__4 Discr=common_bdt
           nBCSVM__4__5 Discr=mem_SL_0w2h2t
              btag_LR_4b_2b_logit__m20_0__8_8 Discr=mem_SL_0w2h2t
              btag_LR_4b_2b_logit__8_8__20_0 Discr=mem_SL_0w2h2t
        numJets__6__8 Discr=common_bdt
           nBCSVM__1__4 Discr=common_bdt
              nBCSVM__1__3 Discr=common_bdt
                 nBCSVM__1__2 Discr=None
                 nBCSVM__2__3 Discr=common_bdt
              nBCSVM__3__4 Discr=common_bdt
           nBCSVM__4__8 Discr=mem_SL_0w2h2t
              btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
              btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_blr"] = """
  Discr=mem_SL_0w2h2t
    numJets__4__5 Discr=mem_SL_0w2h2t 
       nBCSVM__3__4 Discr=btag_LR_4b_2b_logit
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
    numJets__5__8 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__3__4 Discr=btag_LR_4b_2b_logit
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
       numJets__6__8 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t
             nBCSVM__2__3 Discr=btag_LR_4b_2b_logit
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__8 Discr=mem_SL_0w2h2t
"""

trees["old_2t_blr"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__8_0__20_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__4_8__20_0 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__10_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__10_4__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__4_8__20_0 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_2t_blr_A"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=counting
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=counting
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
             btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__8_0__20_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__10_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__10_4__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""


trees["old_2t_blr_B"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=counting
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=counting
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
             btag_LR_4b_2b_logit__6_4__20_0 Discr=counting
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=counting
          btag_LR_4b_2b_logit__8_0__20_0 Discr=counting
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__10_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__10_4__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_2t_blr_C"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=btag_LR_4b_2b_logit
          nBCSVM__3__4 Discr=btag_LR_4b_2b_logit
       nBCSVM__4__5 Discr=btag_LR_4b_2b_logit
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=btag_LR_4b_2b_logit
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__10_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__10_4__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=btag_LR_4b_2b_logit
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_2t_blr_D"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=counting
          nBCSVM__3__4 Discr=counting
       nBCSVM__4__5 Discr=counting
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=btag_LR_4b_2b_logit
             nBCSVM__3__4 Discr=btag_LR_4b_2b_logit
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__10_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__10_4__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=btag_LR_4b_2b_logit
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_2t_blr_E"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=counting
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=counting
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
             btag_LR_4b_2b_logit__6_4__20_0 Discr=counting
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=counting
          btag_LR_4b_2b_logit__8_0__20_0 Discr=counting
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                btag_LR_4b_2b_logit__7_2__20_0 Discr=counting
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__10_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__10_4__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_2t_blr_F"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=counting
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=counting
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
             btag_LR_4b_2b_logit__6_4__20_0 Discr=counting
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=counting
          btag_LR_4b_2b_logit__8_0__20_0 Discr=counting
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                btag_LR_4b_2b_logit__7_2__20_0 Discr=counting
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_2t_blr_G"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=counting
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=counting
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
             btag_LR_4b_2b_logit__6_4__20_0 Discr=counting
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=counting
          btag_LR_4b_2b_logit__8_0__20_0 Discr=counting
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                btag_LR_4b_2b_logit__7_2__20_0 Discr=counting
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__10_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__10_4__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_2t_blr_H"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=counting
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=counting
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
             btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=mem_SL_0w2h2t
          btag_LR_4b_2b_logit__8_0__20_0 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__10_4 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__10_4__20_0 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

# Merged two low yield BLR splits wrt H
trees["old_2t_blr_I"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=counting
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=counting
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
             btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__7_2 Discr=counting
                btag_LR_4b_2b_logit__7_2__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""


trees["old_2t_blr_J"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=mem_SL_0w2h2t
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__m3_2 Discr=counting
             btag_LR_4b_2b_logit__m3_2__20_0 Discr=counting
          nBCSVM__3__4 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__6_4 Discr=counting
             btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t  
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__4_8 Discr=counting
                btag_LR_4b_2b_logit__4_8__20_0 Discr=counting
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__m20_0__6_4 Discr=mem_SL_0w2h2t
                btag_LR_4b_2b_logit__6_4__20_0 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t  
             btag_LR_4b_2b_logit__m20_0__9_6 Discr=mem_SL_0w2h2t
             btag_LR_4b_2b_logit__9_6__20_0 Discr=mem_SL_0w2h2t
"""

trees["old_dl"] = """
  Discr=mem_DL_0w2h2t rebin=6
     nBCSVM__2__3 Discr=mem_DL_0w2h2t rebin=6
        numJets__2__3 Discr=None
        numJets__3__6 Discr=mem_DL_0w2h2t rebin=6
           numJets__3__4 Discr=mem_DL_0w2h2t rebin=6
           numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
     nBCSVM__3__6 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__3__4 Discr=mem_DL_0w2h2t rebin=6
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t rebin=6
              numJets__3__4 Discr=mem_DL_0w2h2t rebin=6
              numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__4__6 Discr=mem_DL_0w2h2t rebin=6
           numJets__1__4 Discr=None
           numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
"""

trees["old_dl_blr"] = """
  Discr=mem_DL_0w2h2t rebin=6
     nBCSVM__2__3 Discr=mem_DL_0w2h2t rebin=6
        numJets__2__3 Discr=None
        numJets__3__6 Discr=mem_DL_0w2h2t rebin=6
           numJets__3__4 Discr=btag_LR_4b_2b_logit rebin=5
           numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
     nBCSVM__3__6 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__3__4 Discr=mem_DL_0w2h2t rebin=6
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t rebin=6
              numJets__3__4 Discr=btag_LR_4b_2b_logit rebin=5
              numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
                 btag_LR_4b_2b_logit__m20_0__4_0 Discr=mem_DL_0w2h2t rebin=6
                 btag_LR_4b_2b_logit__4_0__20_0 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__4__6 Discr=mem_DL_0w2h2t rebin=6
           numJets__1__4 Discr=None
           numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
              btag_LR_4b_2b_logit__m20_0__8_0 Discr=mem_DL_0w2h2t rebin=6
              btag_LR_4b_2b_logit__8_0__20_0 Discr=mem_DL_0w2h2t rebin=6
"""

trees["old_dl_bdt"] = """
  Discr=common_bdt rebin=4
     nBCSVM__2__3 Discr=common_bdt rebin=4
        numJets__2__3 Discr=None
        numJets__3__6 Discr=common_bdt rebin=4
           numJets__3__4 Discr=common_bdt rebin=4
           numJets__4__6 Discr=common_bdt rebin=4
     nBCSVM__3__6 Discr=common_bdt rebin=4
        nBCSVM__3__4 Discr=common_bdt rebin=4
           numJets__2__3 Discr=None
           numJets__3__6 Discr=common_bdt rebin=4
              numJets__3__4 Discr=common_bdt rebin=4
              numJets__4__6 Discr=common_bdt rebin=4
        nBCSVM__4__6 Discr=common_bdt rebin=4
           numJets__1__4 Discr=None
           numJets__4__6 Discr=common_bdt rebin=4
"""

trees["old_dl_mem_bdt"] = """
  Discr=common_bdt rebin=4
     nBCSVM__2__3 Discr=common_bdt rebin=4
        numJets__2__3 Discr=None
        numJets__3__6 Discr=common_bdt rebin=4
           numJets__3__4 Discr=common_bdt rebin=4
           numJets__4__6 Discr=common_bdt rebin=4
     nBCSVM__3__6 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__3__4 Discr=mem_DL_0w2h2t rebin=6
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t rebin=6
              numJets__3__4 Discr=common_bdt rebin=4
              numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__4__6 Discr=mem_DL_0w2h2t rebin=6
           numJets__1__4 Discr=None
           numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
"""

trees["old_dl_mem_bdt_blrsplit"] = """
  Discr=common_bdt rebin=4
     nBCSVM__2__3 Discr=common_bdt rebin=4
        numJets__2__3 Discr=None
        numJets__3__6 Discr=common_bdt rebin=4
           numJets__3__4 Discr=common_bdt rebin=4
           numJets__4__6 Discr=common_bdt rebin=4
     nBCSVM__3__6 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__3__4 Discr=mem_DL_0w2h2t rebin=6
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t rebin=6
              numJets__3__4 Discr=mem_DL_0w2h2t rebin=6
              numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
                 btag_LR_4b_2b_logit__m20_0__4_0 Discr=mem_DL_0w2h2t rebin=6
                 btag_LR_4b_2b_logit__4_0__20_0 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__4__6 Discr=mem_DL_0w2h2t rebin=6
           numJets__1__4 Discr=None
           numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
              btag_LR_4b_2b_logit__m20_0__8_0 Discr=mem_DL_0w2h2t rebin=6
              btag_LR_4b_2b_logit__8_0__20_0 Discr=mem_DL_0w2h2t rebin=6
"""

trees["old_dl_mem_bdt_2d"] = """
  Discr=common_bdt rebin=4
     nBCSVM__2__3 Discr=common_bdt rebin=4
        numJets__2__3 Discr=None
        numJets__3__6 Discr=common_bdt rebin=4
           numJets__3__4 Discr=common_bdt rebin=4
           numJets__4__6 Discr=common_bdt rebin=4
     nBCSVM__3__6 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__3__4 Discr=mem_DL_0w2h2t rebin=6
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t rebin=6
              numJets__3__4 Discr=mem_DL_0w2h2t rebin=6
              numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
                 common_bdt__m1_0__0_0 Discr=mem_DL_0w2h2t rebin=6
                 common_bdt__0_0__1_0 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__4__6 Discr=mem_DL_0w2h2t rebin=6
           numJets__1__4 Discr=None
           numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
              common_bdt__m1_0__0_0 Discr=mem_DL_0w2h2t rebin=6
              common_bdt__0_0__1_0 Discr=mem_DL_0w2h2t rebin=6
"""

trees["old_dl_mem_bdt_2d_4bins"] = """
  Discr=common_bdt rebin=4
     nBCSVM__2__3 Discr=common_bdt rebin=4
        numJets__2__3 Discr=None
        numJets__3__6 Discr=common_bdt rebin=4
           numJets__3__4 Discr=common_bdt rebin=4
           numJets__4__6 Discr=common_bdt rebin=4
     nBCSVM__3__6 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__3__4 Discr=mem_DL_0w2h2t rebin=6
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t rebin=6
              numJets__3__4 Discr=mem_DL_0w2h2t rebin=6
              numJets__4__6 Discr=mem_DL_0w2h2t rebin=6
                 common_bdt__m1_0__0_0 Discr=mem_DL_0w2h2t rebin=6
                 common_bdt__0_0__1_0 Discr=mem_DL_0w2h2t rebin=6
        nBCSVM__4__6 Discr=mem_DL_0w2h2t rebin=12
           numJets__1__4 Discr=None
           numJets__4__6 Discr=mem_DL_0w2h2t rebin=12
              common_bdt__m1_0__0_0 Discr=mem_DL_0w2h2t rebin=12
              common_bdt__0_0__1_0 Discr=mem_DL_0w2h2t rebin=12
"""

trees["old_dl_parity"] = """
  Discr=mem_DL_0w2h2t
     eventParity__0__1 Discr=mem_SL_0w2h2t
        nBCSVM__2__3 Discr=mem_DL_0w2h2t
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t
              numJets__3__4 Discr=mem_DL_0w2h2t
              numJets__4__6 Discr=mem_DL_0w2h2t
        nBCSVM__3__6 Discr=mem_DL_0w2h2t
           nBCSVM__3__4 Discr=mem_DL_0w2h2t
              numJets__2__3 Discr=None
              numJets__3__6 Discr=mem_DL_0w2h2t
           nBCSVM__4__6 Discr=mem_DL_0w2h2t
              numJets__1__4 Discr=None
              numJets__4__6 Discr=mem_DL_0w2h2t
     eventParity__1__2 Discr=mem_SL_0w2h2t
        nBCSVM__2__3 Discr=mem_DL_0w2h2t
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t
              numJets__3__4 Discr=mem_DL_0w2h2t
              numJets__4__6 Discr=mem_DL_0w2h2t
        nBCSVM__3__6 Discr=mem_DL_0w2h2t
           nBCSVM__3__4 Discr=mem_DL_0w2h2t
              numJets__2__3 Discr=None
              numJets__3__6 Discr=mem_DL_0w2h2t
           nBCSVM__4__6 Discr=mem_DL_0w2h2t
              numJets__1__4 Discr=None
              numJets__4__6 Discr=mem_DL_0w2h2t
"""


# Optimization on tree with BLR < 0.95 preselection cut
# BDT not included as discriminator
# 7 Categories
trees["with_blrcut_no_bdt"] = """
  Discr=2
    btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
          numJets__4__6 Discr=2
          numJets__6__7 Discr=2
    btag_LR_4b_2b_logit__8_0__20_0 Discr=2
       n_excluded_bjets__0__1 Discr=2
          numJets__4__5 Discr=2 S=2.1
          numJets__5__7 Discr=2 S=8.0
       n_excluded_bjets__1__4 Discr=2
          n_excluded_ljets__0__2 Discr=2
          n_excluded_ljets__2__4 Discr=2
"""

# Opt on tree with BLR < 0.95 preselection cut
# BDT included as discriminator
# 7 categories
trees["with_blrcut_bdr"] = """
  Discr=2
    nBCSVM__2__4 Discr=3
       nBCSVM__2__3 Discr=2
       nBCSVM__3__4 Discr=3
          Wmass__40_0__53_3333333333 Discr=3
          Wmass__53_3333333333__120_0 Discr=2
    nBCSVM__4__5 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
             numJets__4__5 Discr=2
             numJets__5__7 Discr=2
          n_excluded_bjets__1__4 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT included as discriminator
# 7 categories
trees["no_blrcut_with_bdt"] = """
  Discr=2
    btag_LR_4b_2b_logit__m20_0__8_0 Discr=3
       btag_LR_4b_2b_logit__m20_0__4_0 Discr=3
          nBCSVM__2__3 Discr=3
          nBCSVM__3__5 Discr=2
       btag_LR_4b_2b_logit__4_0__8_0 Discr=2
          numJets__4__5 Discr=3
          numJets__5__7 Discr=2
             n_excluded_bjets__0__1 Discr=2
             n_excluded_bjets__1__4 Discr=2
    btag_LR_4b_2b_logit__8_0__20_0 Discr=2
       n_excluded_bjets__0__1 Discr=2
       n_excluded_bjets__1__4 Discr=2
"""


# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 1 categories
trees["1cat"] = """
  Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 2 categories
#trees["3cat"] = """
#  Discr=2
#    numJets__4__5 Discr=2
#    numJets__5__8 Discr=2
#       numJets__5__6 Discr=2
#       numJets__6__8 Discr=2
#"""

trees["3cat"] = """
  Discr=mem_SL_0w2h2t
    numJets__4__5 Discr=mem_SL_0w2h2t
    numJets__5__8 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
       numJets__6__8 Discr=mem_SL_0w2h2t
"""


# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 3 categories
#trees["3cat"] = """
#  Discr=2
#    numJets__4__5 Discr=2
#    numJets__5__7 Discr=2
#       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
#       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
#"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 4 categories
trees["4cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 5 categories
trees["5cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 6 categories
trees["6cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 7 categories
trees["7cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 8 categories
trees["8cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
                topCandidate_mass__100_0__150_0 Discr=2
                topCandidate_mass__150_0__200_0 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
"""


# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 9 categories
trees["9cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
                topCandidate_mass__100_0__150_0 Discr=2
                topCandidate_mass__150_0__200_0 Discr=2
                   n_excluded_ljets__0__2 Discr=2
                   n_excluded_ljets__2__4 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 10 categories
trees["10cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
             n_excluded_ljets__0__2 Discr=2
             n_excluded_ljets__2__4 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
                topCandidate_mass__100_0__150_0 Discr=2
                topCandidate_mass__150_0__200_0 Discr=2
                   n_excluded_ljets__0__2 Discr=2
                   n_excluded_ljets__2__4 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 11 categories
trees["11cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
             n_excluded_ljets__0__2 Discr=2
             n_excluded_ljets__2__4 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
                topCandidate_mass__100_0__150_0 Discr=2
                topCandidate_mass__150_0__200_0 Discr=2
                   n_excluded_ljets__0__2 Discr=2
                   n_excluded_ljets__2__4 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
                n_excluded_ljets__0__2 Discr=2
                n_excluded_ljets__2__4 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 12 categories
trees["12cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
             n_excluded_ljets__0__2 Discr=2
             n_excluded_ljets__2__4 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
                topCandidate_mass__100_0__150_0 Discr=2
                topCandidate_mass__150_0__200_0 Discr=2
                   n_excluded_ljets__0__2 Discr=2
                      topCandidate_fRec__0_0__0_20000000298 Discr=2
                      topCandidate_fRec__0_20000000298__0_40000000596 Discr=2
                   n_excluded_ljets__2__4 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
                n_excluded_ljets__0__2 Discr=2
                n_excluded_ljets__2__4 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 13 categories
trees["13cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__8_0__20_0 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
             n_excluded_ljets__0__2 Discr=2
             n_excluded_ljets__2__4 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
                topCandidate_mass__100_0__150_0 Discr=2
                topCandidate_mass__150_0__200_0 Discr=2
                   n_excluded_ljets__0__2 Discr=2
                      topCandidate_fRec__0_0__0_20000000298 Discr=2
                      topCandidate_fRec__0_20000000298__0_40000000596 Discr=2
                   n_excluded_ljets__2__4 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
                n_excluded_ljets__0__2 Discr=2
                n_excluded_ljets__2__4 Discr=2
"""



# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 14 categories
trees["14cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__8_0__20_0 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
             n_excluded_ljets__0__2 Discr=2
             n_excluded_ljets__2__4 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
                topCandidate_mass__100_0__150_0 Discr=2
                topCandidate_mass__150_0__200_0 Discr=2
                   n_excluded_ljets__0__2 Discr=2
                      topCandidate_fRec__0_0__0_20000000298 Discr=2
                      topCandidate_fRec__0_20000000298__0_40000000596 Discr=2
                   n_excluded_ljets__2__4 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
                n_excluded_ljets__0__2 Discr=2
                n_excluded_ljets__2__4 Discr=2
                   topCandidate_mass__100_0__133_333333333 Discr=2
                   topCandidate_mass__133_333333333__200_0 Discr=2
"""

# Opt on tree without BLR preselection cut
# BDT NOT included as discriminator
# 15 categories
trees["15cat"] = """
  Discr=2
    numJets__4__5 Discr=2
       nBCSVM__2__3 Discr=2
       nBCSVM__3__5 Discr=2
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__8_0__20_0 Discr=2
    numJets__5__7 Discr=2
       btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
          btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
          btag_LR_4b_2b_logit__4_0__8_0 Discr=2
             n_excluded_ljets__0__2 Discr=2
             n_excluded_ljets__2__4 Discr=2
       btag_LR_4b_2b_logit__8_0__20_0 Discr=2
          n_excluded_bjets__0__1 Discr=2
          n_excluded_bjets__1__4 Discr=2
             topCandidate_n_subjettiness__0_0__0_666666666667 Discr=2
                topCandidate_mass__100_0__150_0 Discr=2
                topCandidate_mass__150_0__200_0 Discr=2
                   n_excluded_ljets__0__2 Discr=2
                      topCandidate_fRec__0_0__0_20000000298 Discr=2
                      topCandidate_fRec__0_20000000298__0_40000000596 Discr=2
                   n_excluded_ljets__2__4 Discr=2
             topCandidate_n_subjettiness__0_666666666667__1_0 Discr=2
                n_excluded_ljets__0__2 Discr=2
                   topCandidate_fRec__0_0__0_3333333383 Discr=2
                   topCandidate_fRec__0_3333333383__0_40000000596 Discr=2
                n_excluded_ljets__2__4 Discr=2
                   topCandidate_mass__100_0__133_333333333 Discr=2
                   topCandidate_mass__133_333333333__200_0 Discr=2
"""



#trees["6j_4t"] = """
#  Discr=common_bdt
#    numJets__3__5 Discr=None
#    numJets__5__7 Discr=common_bdt
#       numJets__5__6 Discr=None
#       numJets__6__7 Discr=common_bdt
#          nBCSVM__1__4 Discr=None
#          nBCSVM__4__5 Discr=common_bdt
#"""
#
trees["6j_4t_memsplit"] = """
  Discr=common_bdt
    numJets__3__5 Discr=None
    numJets__5__7 Discr=common_bdt
       numJets__5__6 Discr=None
       numJets__6__7 Discr=common_bdt
          nBCSVM__1__4 Discr=None
          nBCSVM__4__5 Discr=common_bdt
             mem_SL_0w2h2t__0_0__0_833333333333 Discr=common_bdt
             mem_SL_0w2h2t__0_833333333333__1_0 Discr=common_bdt
"""

trees["6j_4t"] = """
  Discr=counting
    eventParity__0__1 Discr=None
    eventParity__1__2 Discr=counting
        numJets__3__5 Discr=None
        numJets__5__7 Discr=counting
           numJets__5__6 Discr=None
           numJets__6__7 Discr=counting
              nBCSVM__1__4 Discr=None
              nBCSVM__4__5 Discr=counting
"""

trees["6j_4t_bdt"] = """
  Discr=common_bdt rebin=5
    eventParity__0__1 Discr=common_bdt rebin=5
       numJets__3__5 Discr=None
       numJets__5__7 Discr=common_bdt rebin=5
          numJets__5__6 Discr=None
          numJets__6__7 Discr=common_bdt rebin=5
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=common_bdt rebin=5
    eventParity__1__2 Discr=common_bdt rebin=5
       numJets__3__5 Discr=None
       numJets__5__7 Discr=common_bdt rebin=5
          numJets__5__6 Discr=None
          numJets__6__7 Discr=common_bdt rebin=5
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=common_bdt rebin=5
"""

trees["6j_4t_mem"] = """
  Discr=mem_SL_0w2h2t rebin=6
    eventParity__0__1 Discr=mem_SL_0w2h2t rebin=6
       numJets__3__5 Discr=None
       numJets__5__7 Discr=mem_SL_0w2h2t rebin=6
          numJets__5__6 Discr=None
          numJets__6__7 Discr=mem_SL_0w2h2t rebin=6
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
    eventParity__1__2 Discr=mem_SL_0w2h2t rebin=6
       numJets__3__5 Discr=None
       numJets__5__7 Discr=mem_SL_0w2h2t rebin=6
          numJets__5__6 Discr=None
          numJets__6__7 Discr=mem_SL_0w2h2t rebin=6
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=mem_SL_0w2h2t rebin=6
"""

trees["6j_4t_test2"] = """
  Discr=counting
    eventParity__0__1 Discr=counting
       numJets__3__5 Discr=None
       numJets__5__7 Discr=counting
          numJets__5__6 Discr=None
          numJets__6__7 Discr=counting
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=counting
                common_bdt__m1_0__0_15 Discr=counting
                   mem_SL_0w2h2t__0_0__0_416666666667 Discr=counting
                      mem_SL_0w2h2t__0_0__0_0277777777778 Discr=counting
                      mem_SL_0w2h2t__0_0277777777778__0_416666666667 Discr=counting
                         common_bdt__m1_0__m0_1 Discr=counting
                         common_bdt__m0_1__0_15 Discr=counting
                   mem_SL_0w2h2t__0_416666666667__1_0 Discr=counting
                common_bdt__0_15__1_0 Discr=counting             
    eventParity__1__2 Discr=counting
       numJets__3__5 Discr=None
       numJets__5__7 Discr=counting
          numJets__5__6 Discr=None
          numJets__6__7 Discr=counting
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=counting
                common_bdt__m1_0__0_15 Discr=counting
                   mem_SL_0w2h2t__0_0__0_416666666667 Discr=counting
                      mem_SL_0w2h2t__0_0__0_0277777777778 Discr=counting
                      mem_SL_0w2h2t__0_0277777777778__0_416666666667 Discr=counting
                         common_bdt__m1_0__m0_1 Discr=counting
                         common_bdt__m0_1__0_15 Discr=counting
                   mem_SL_0w2h2t__0_416666666667__1_0 Discr=counting
                common_bdt__0_15__1_0 Discr=counting             
"""

# Split only by BDR
trees["6j_4t_test3"] = """
  Discr=counting
    eventParity__0__1 Discr=counting
       numJets__3__5 Discr=None
       numJets__5__7 Discr=counting
          numJets__5__6 Discr=None
          numJets__6__7 Discr=counting
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=counting
                common_bdt__m1_0__0_15 Discr=counting
                   common_bdt__m1_0__m0_15 Discr=counting
                      common_bdt__m1_0__m0_3 Discr=counting
                      common_bdt__m0_3__m0_15 Discr=counting 
                   common_bdt__m0_15__0_15 Discr=counting
                      common_bdt__m0_15__0_0 Discr=counting
                      common_bdt__0_0__0_15 Discr=counting
                common_bdt__0_15__1_0 Discr=counting
    eventParity__1__2 Discr=counting
       numJets__3__5 Discr=None
       numJets__5__7 Discr=counting
          numJets__5__6 Discr=None
          numJets__6__7 Discr=counting
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=counting
                common_bdt__m1_0__0_15 Discr=counting
                   common_bdt__m1_0__m0_15 Discr=counting
                      common_bdt__m1_0__m0_3 Discr=counting
                      common_bdt__m0_3__m0_15 Discr=counting
                   common_bdt__m0_15__0_15 Discr=counting
                      common_bdt__m0_15__0_0 Discr=counting
                      common_bdt__0_0__0_15 Discr=counting
                common_bdt__0_15__1_0 Discr=counting
"""

# Split only by MEM
trees["6j_4t_test4"] = """
  Discr=counting
    eventParity__0__1 Discr=counting
       numJets__3__5 Discr=None
       numJets__5__7 Discr=counting
          numJets__5__6 Discr=None
          numJets__6__7 Discr=counting
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=counting
                 mem_SL_0w2h2t__0_0__0_361111111111 Discr=counting
                    mem_SL_0w2h2t__0_0__0_0277777777778 Discr=counting
                    mem_SL_0w2h2t__0_0277777777778__0_361111111111 Discr=counting
                       mem_SL_0w2h2t__0_0277777777778__0_194444444444 Discr=counting
                       mem_SL_0w2h2t__0_194444444444__0_361111111111 Discr=counting
                 mem_SL_0w2h2t__0_361111111111__1_0 Discr=counting
                    mem_SL_0w2h2t__0_361111111111__0_611111111111 Discr=counting
                    mem_SL_0w2h2t__0_611111111111__1_0 Discr=counting
    eventParity__1__2 Discr=counting
       numJets__3__5 Discr=None
       numJets__5__7 Discr=counting
          numJets__5__6 Discr=None
          numJets__6__7 Discr=counting
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=counting
                 mem_SL_0w2h2t__0_0__0_361111111111 Discr=counting
                    mem_SL_0w2h2t__0_0__0_0277777777778 Discr=counting
                    mem_SL_0w2h2t__0_0277777777778__0_361111111111 Discr=counting
                       mem_SL_0w2h2t__0_0277777777778__0_194444444444 Discr=counting
                       mem_SL_0w2h2t__0_194444444444__0_361111111111 Discr=counting
                 mem_SL_0w2h2t__0_361111111111__1_0 Discr=counting
                    mem_SL_0w2h2t__0_361111111111__0_611111111111 Discr=counting
                    mem_SL_0w2h2t__0_611111111111__1_0 Discr=counting

"""


#
#                mem_SL_0w2h2t__0_0__0_75 Discr=counting
#                   mem_SL_0w2h2t__0_0__0_222222222222 Discr=counting
#                      common_bdt__m1_0__0_05 Discr=counting
#                      common_bdt__0_05__1_0 Discr=counting
#                         common_bdt__0_05__0_1 Discr=counting
#                         common_bdt__0_1__1_0 Discr=counting  
#                   mem_SL_0w2h2t__0_222222222222__0_75 Discr=counting
#                      common_bdt__m1_0__0_35 Discr=counting
#                      common_bdt__0_35__1_0 Discr=counting 
#                mem_SL_0w2h2t__0_75__1_0 Discr=counting
#                   common_bdt__m1_0__0_0 Discr=counting
#                   common_bdt__0_0__1_0 Discr=counting
#                      common_bdt__0_0__0_3 Discr=counting
#                      common_bdt__0_3__1_0 Discr=counting
#                         mem_SL_0w2h2t__0_75__0_888888888889 Discr=counting
#                         mem_SL_0w2h2t__0_888888888889__1_0 Discr=counting      
#
trees["6j_4t_test"] = """
  Discr=counting
    eventParity__0__1 Discr=counting
       numJets__3__5 Discr=None
       numJets__5__7 Discr=counting
          numJets__5__6 Discr=None
          numJets__6__7 Discr=counting
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=counting
                mem_SL_0w2h2t__0_0__0_75 Discr=counting                                      
                   mem_SL_0w2h2t__0_0__0_222222222222 Discr=counting            
                      common_bdt__m1_0__0_05 Discr=counting                     
                      common_bdt__0_05__1_0 Discr=counting                      
                         common_bdt__0_05__0_1 Discr=counting                   
                         common_bdt__0_1__1_0 Discr=counting                    
                   mem_SL_0w2h2t__0_222222222222__0_75 Discr=counting           
                      common_bdt__m1_0__0_35 Discr=counting                     
                      common_bdt__0_35__1_0 Discr=counting                      
                mem_SL_0w2h2t__0_75__1_0 Discr=counting                         
                   common_bdt__m1_0__0_0 Discr=counting                         
                   common_bdt__0_0__1_0 Discr=counting                          
                      common_bdt__0_0__0_3 Discr=counting                       
                      common_bdt__0_3__1_0 Discr=counting                       
    eventParity__1__2 Discr=counting
       numJets__3__5 Discr=None
       numJets__5__7 Discr=counting
          numJets__5__6 Discr=None
          numJets__6__7 Discr=counting
             nBCSVM__1__4 Discr=None
             nBCSVM__4__5 Discr=counting
                mem_SL_0w2h2t__0_0__0_75 Discr=counting                                      
                   mem_SL_0w2h2t__0_0__0_222222222222 Discr=counting            
                      common_bdt__m1_0__0_05 Discr=counting                     
                      common_bdt__0_05__1_0 Discr=counting                      
                         common_bdt__0_05__0_1 Discr=counting                   
                         common_bdt__0_1__1_0 Discr=counting                    
                   mem_SL_0w2h2t__0_222222222222__0_75 Discr=counting           
                      common_bdt__m1_0__0_35 Discr=counting                     
                      common_bdt__0_35__1_0 Discr=counting                      
                mem_SL_0w2h2t__0_75__1_0 Discr=counting                         
                   common_bdt__m1_0__0_0 Discr=counting                         
                   common_bdt__0_0__1_0 Discr=counting                          
                      common_bdt__0_0__0_3 Discr=counting                       
                      common_bdt__0_3__1_0 Discr=counting                       
                         mem_SL_0w2h2t__0_75__0_888888888889 Discr=counting     
                         mem_SL_0w2h2t__0_888888888889__1_0 Discr=counting      
"""



trees["6j_4t_doublememsplit"] = """
  Discr=common_bdt
    numJets__3__5 Discr=None
    numJets__5__7 Discr=common_bdt
       numJets__5__6 Discr=None
       numJets__6__7 Discr=common_bdt
          nBCSVM__1__4 Discr=None
          nBCSVM__4__5 Discr=common_bdt
             mem_SL_0w2h2t__0_0__0_833333333333 Discr=common_bdt
                mem_SL_0w2h2t__0_0__0_166666666667 Discr=common_bdt
                mem_SL_0w2h2t__0_166666666667__0_833333333333 Discr=common_bdt
             mem_SL_0w2h2t__0_833333333333__1_0 Discr=common_bdt
                mem_SL_0w2h2t__0_833333333333__0_916666666667 Discr=common_bdt
                mem_SL_0w2h2t__0_916666666667__1_0 Discr=common_bdt
"""



trees["6j_4t_doublebdtsplit"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=None
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=None
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=None
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
                common_bdt__m1_0__m0_333333333333 Discr=mem_SL_0w2h2t
                common_bdt__m0_333333333333__0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
                common_bdt__0_166666666667__0_333333333333 Discr=mem_SL_0w2h2t
                common_bdt__0_333333333333__1_0 Discr=mem_SL_0w2h2t
"""

trees["6j_4t_bdtsplit"] = """
  Discr=mem_SL_0w2h2t
    numJets__3__5 Discr=None
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=None
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__1__4 Discr=None
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
             common_bdt__m1_0__0_166666666667 Discr=mem_SL_0w2h2t
             common_bdt__0_166666666667__1_0 Discr=mem_SL_0w2h2t
"""
