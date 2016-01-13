import sys
import matplotlib
matplotlib.use('Agg')
sys.path += ["/Users/joosep/Documents/heplot/"]
import heplot, rootpy
import numpy as np
import matplotlib.pyplot as plt
import pandas
import rootpy.plotting.root2matplotlib as rplt
import ROOT, plotlib, heplot
import tabulate
import cPickle as pickle
from collections import OrderedDict

#Categorizer
sys.path.append("/Users/joosep/Documents/tth/sw-slc6/CMSSW_7_4_15/src/TTH/Plotting/python/Datacards/")
import Categorize, Forest, TreeAnalysis
import Cut


sl_channels = ["sl_j4_t2", "sl_j4_t3", "sl_j4_t4", "sl_j5_t2", "sl_j5_t3", "sl_j5_tge4", "sl_jge6_t2", "sl_jge6_t3", "sl_jge6_tge4"]
sl_channels_flavoursplit = ["sl_mu_j4_t2", "sl_mu_j4_t3", "sl_mu_j4_t4", "sl_mu_j5_t2", "sl_mu_j5_t3", "sl_mu_j5_tge4", "sl_mu_jge6_t2", "sl_mu_jge6_t3", "sl_mu_jge6_tge4"]
dl_channels = ["dl_j3_t2", "dl_jge3_t3", "dl_jge4_t2", "dl_jge4_tge4"]
dl_channels_flavoursplit = ["dl_mumu_j3_t2", "dl_mumu_jge3_t3", "dl_mumu_jge4_t2", "dl_mumu_jge4_tge4"]

backgrounds = ["ttbarOther", "ttbarPlusBBbar", "ttbarPlusB", "ttbarPlus2B", "ttbarPlusCCbar"]

def writeSyncTable(inf, channels, title):
    #outfile.write("<h2>{0}</h2>\n".format(title))
    table_hists, table = plotlib.sync_table(
        inf,
        channels,
        backgrounds
    )
    # outfile.write(
    #     tabulate.tabulate(table, tablefmt="html", headers=channels)
    # )
    of = open("tables/{0}.csv".format(title), "w")
    of.write(tabulate.tabulate(table, tablefmt="plain", headers=channels))
    of.close()
    print tabulate.tabulate(table, headers=channels)

input_file = "/Users/joosep/Dropbox/tth/ControlPlotsSparse.root"
inf = rootpy.io.File(input_file)

writeSyncTable(inf, sl_channels, "sl")

writeSyncTable(inf, sl_channels_flavoursplit, "sl_mu")
writeSyncTable(inf, [ch.replace("mu", "el") for ch in sl_channels_flavoursplit], "sl_el")

writeSyncTable(inf, dl_channels, "dl")
writeSyncTable(inf, dl_channels_flavoursplit, "dl_mumu")
writeSyncTable(inf, [ch.replace("mumu", "ee") for ch in dl_channels_flavoursplit], "dl_ee")
writeSyncTable(inf, [ch.replace("mumu", "emu") for ch in dl_channels_flavoursplit], "dl_emu")
