
trees = {}

# Classic categorization:
# Based on jet and tagged jet multiplicity
# 7 categories
trees["old"] = """
  Discr=mem_SL_0w2h2t
    numJets__4__5 Discr=mem_SL_0w2h2t 
       nBCSVM__3__4 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
    numJets__5__7 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
       numJets__6__7 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
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

#trees["old"] = """
#  Discr=mem_SL_0w2h2t
#    numJets__4__5 Discr=mem_SL_0w2h2t 
#       nBCSVM__3__4 Discr=mem_SL_0w2h2t
#       nBCSVM__4__5 Discr=mem_SL_0w2h2t
#"""

trees["old_dl"] = """
  Discr=mem_DL_0w2h2t
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

# Classic categorization:
# Based on jet and tagged jet multiplicity. Also include the 2tag bins.
# 7 categories + 2 categories (4j2t, 5j2t)
trees["old_2t"] = """
  Discr=mem_SL_0w2h2t 
    numJets__4__5 Discr=mem_SL_0w2h2t 
       nBCSVM__2__4 Discr=mem_SL_0w2h2t
          nBCSVM__2__3 Discr=mem_SL_0w2h2t
          nBCSVM__3__4 Discr=mem_SL_0w2h2t
       nBCSVM__4__5 Discr=mem_SL_0w2h2t
    numJets__5__8 Discr=mem_SL_0w2h2t
       numJets__5__6 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__5 Discr=mem_SL_0w2h2t
       numJets__6__8 Discr=mem_SL_0w2h2t
          nBCSVM__2__4 Discr=mem_SL_0w2h2t
             nBCSVM__2__3 Discr=mem_SL_0w2h2t
             nBCSVM__3__4 Discr=mem_SL_0w2h2t
          nBCSVM__4__8 Discr=mem_SL_0w2h2t
"""

# Classic categorization using jets and tagged jet multiplicity
# Each final category is subdivded by BLR
# 14 categories
trees["old_blrsplit"] = """
  Discr=2
    numJets__4__5 Discr=2 
       nBCSVM__2__4 Discr=2
          nBCSVM__2__3 Discr=-1
          nBCSVM__3__4 Discr=2
             btag_LR_4b_2b_logit__m20_0__4_0 Discr=2 
             btag_LR_4b_2b_logit__4_0__20_0 Discr=2 
       nBCSVM__4__5 Discr=2 j4t4
          btag_LR_4b_2b_logit__m20_0__8_0 Discr=2 
          btag_LR_4b_2b_logit__8_0__20_0 Discr=2 
    numJets__5__7 Discr=2
       numJets__5__6 Discr=2
          nBCSVM__2__4 Discr=2 
             nBCSVM__2__3 Discr=-1
             nBCSVM__3__4 Discr=2 j5t3
                btag_LR_4b_2b_logit__m20_0__4_0 Discr=2 
                btag_LR_4b_2b_logit__4_0__20_0 Discr=2 
          nBCSVM__4__5 Discr=2 j5t4
             btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
             btag_LR_4b_2b_logit__8_0__20_0 Discr=2
       numJets__6__7 Discr=2
          nBCSVM__2__4 Discr=2
             nBCSVM__2__3 Discr=2
                btag_LR_4b_2b_logit__m20_0__0_0 Discr=2
                btag_LR_4b_2b_logit__0_0__20_0 Discr=2
             nBCSVM__3__4 Discr=2
                btag_LR_4b_2b_logit__m20_0__4_0 Discr=2
                btag_LR_4b_2b_logit__4_0__20_0 Discr=2
          nBCSVM__4__5 Discr=2
             btag_LR_4b_2b_logit__m20_0__8_0 Discr=2
             btag_LR_4b_2b_logit__8_0__20_0 Discr=2
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
