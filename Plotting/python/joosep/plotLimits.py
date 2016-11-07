import ROOT
import rootpy
import math
import matplotlib
matplotlib.use('GTKAgg') 
import matplotlib.pyplot as plt
from rootpy.plotting import root2matplotlib as rplt

import sys
sys.path += ["/Users/joosep/Documents/heplot"]
import heplot

import sparse
import plotlib
import os

from rootpy.plotting import Hist
from collections import OrderedDict




cats = [
    "AnalysisSpecification/0/higgsCombineshapes_group_sl_jge6_t2_mem_SL_0w2h2t.Asymptotic.mH120.root",
    "AnalysisSpecification/1/higgsCombineshapes_group_sl_j4_tge4_mem_SL_0w2h2t.Asymptotic.mH120.root",
    "AnalysisSpecification/2/higgsCombineshapes_group_sl_j5_t3_mem_SL_0w2h2t.Asymptotic.mH120.root",
    "AnalysisSpecification/3/higgsCombineshapes_group_sl_jge6_tge4_mem_SL_0w2h2t.Asymptotic.mH120.root",
    "AnalysisSpecification/4/higgsCombineshapes_group_sl_j4_t3_mem_SL_0w2h2t.Asymptotic.mH120.root",
    "AnalysisSpecification/5/higgsCombineshapes_group_sl.Asymptotic.mH120.root",
    "AnalysisSpecification/6/higgsCombineshapes_group_sl_jge6_t3_mem_SL_0w2h2t.Asymptotic.mH120.root",
    "AnalysisSpecification/7/higgsCombineshapes_group_sl_j5_tge4_mem_SL_0w2h2t.Asymptotic.mH120.root",
]
