trees = {}

# Formerly known as old
# 7 Categories
# Fit MEM in each category
# Use 6 bins for MEM in each category
# NOT split by parity
trees["mem_6bin"] = """
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

# 7 Categories
# Fit MEM in each category
# Use 6 bins for MEM in each category
# Split by parity
trees["mem_6bin_parity"] = """
  Discr=mem_SL_0w2h2t
     eventParity__0__1 Discr=mem_SL_0w2h2t
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
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6       
     eventParity__1__2 Discr=mem_SL_0w2h2t
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
                 nBCSVM__1__3 Discr=mem_SL_0w2h2t
                    nBCSVM__1__2 Discr=None
                    nBCSVM__2__3 Discr=mem_SL_0w2h2t rebin=6
                 nBCSVM__3__4 Discr=mem_SL_0w2h2t rebin=6
              nBCSVM__4__8 Discr=mem_SL_0w2h2t rebin=6       
"""


# Formerly known as old_rebin_parity
# 7 categories
# Fit MEM in each category
# 18 bins for 2t and 3t, 9 bins for 4j4t and 5j4t, 6 bins for 6j4t
# NOT split by parity
trees["mem_betterbin"] = """
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

# Formerly known as 7cat_mem_betterbin
# 7 categories
# Fit MEM in each category
# 18 bins for 2t and 3t, 9 bins for 4j4t and 5j4t, 6 bins for 6j4t
# Split by parity
trees["mem_betterbin_parity"] = """
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

# 7 categories
# Fit BDT in each category
# 20 bins for 2t and 3t, 10 bins for 4j4t and 5j4t, 8 bins for 6j4t
# Split by parity
trees["bdt_betterbin_parity"] = """
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


# Formerly known as 7cat_mem_betterbin
# 2x7 categories (BDT lo and BDT high)
# Fit MEM in each category
# 2x9 bins for 2t and 3t, 2x6 bins for 4j4t, 5j4t and 6j4t
# Split by parity
trees["2d_all_parity"] = """
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

# Formerly known as old_mem_bdt2d_2tbdt
# "Option D"
# 2x6 + 1 categories (BDT lo and BDT high) 
# Fit MEM in everywhere except 6j2t (fit BDT there)
# 2x9 bins for 3t, 2x6 bins for 4j4t, 5j4t and 6j4t, 20 bins for 6j2t
# Split by parity
trees["2d_3t4t_parity"] = """
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

#'dl_j3_t2': -1.3,
# 'dl_jge3_tge3': 3.8,
# 'dl_jge4_t2': -0.7,
# 'dl_jge4_tge4': 7.7,

trees["old_dl_blrsplit"] = """
  Discr=mem_DL_0w2h2t
     nBCSVM__2__3 Discr=mem_DL_0w2h2t
        numJets__2__3 Discr=None
        numJets__3__6 Discr=mem_DL_0w2h2t
           numJets__3__4 Discr=mem_DL_0w2h2t
              btag_LR_4b_2b_logit__m20_0__m1_6 Discr=mem_DL_0w2h2t
              btag_LR_4b_2b_logit__m1_6__20_0 Discr=mem_DL_0w2h2t
           numJets__4__6 Discr=mem_DL_0w2h2t
              btag_LR_4b_2b_logit__m20_0__m0_8 Discr=mem_DL_0w2h2t
              btag_LR_4b_2b_logit__m0_8__20_0 Discr=mem_DL_0w2h2t
     nBCSVM__3__6 Discr=mem_DL_0w2h2t
        nBCSVM__3__4 Discr=mem_DL_0w2h2t
           numJets__2__3 Discr=None
           numJets__3__6 Discr=mem_DL_0w2h2t
              btag_LR_4b_2b_logit__m20_0__4_0 Discr=mem_DL_0w2h2t
              btag_LR_4b_2b_logit__4_0__20_0 Discr=mem_DL_0w2h2t
        nBCSVM__4__6 Discr=mem_DL_0w2h2t
           numJets__1__4 Discr=None
           numJets__4__6 Discr=mem_DL_0w2h2t
             btag_LR_4b_2b_logit__m20_0__8_0 Discr=mem_DL_0w2h2t
              btag_LR_4b_2b_logit__8_0__20_0 Discr=mem_DL_0w2h2t
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
