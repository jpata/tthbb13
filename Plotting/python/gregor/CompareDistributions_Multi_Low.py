#!/usr/bin/env python
"""
"""

########################################
# Imports
########################################

import os
import sys
import pickle
import socket # to get the hostname

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.gregor.TopTaggingVariables import *
    from TTH.Plotting.gregor.TopSamples import *
else:
    from TTH.Plotting.python.Helpers.CompareDistributionsHelpers import *
    from TTH.Plotting.python.gregor.TopTaggingVariables import *
    from TTH.Plotting.python.gregor.TopSamples import *

########################################
# Define Input Files and
# output directory
########################################

if socket.gethostname() == "t3ui12":
    basepath = '/scratch/gregor/'
else:
    basepath = '/Users/gregor/'
                                         
# for the filename: basepath + filename + .root
full_file_names = {}
for k,v in files.iteritems():
    full_file_names[k] = basepath + v + "-weighted.root"

output_dir = "/shome/gregor/new_results/CompareDistributions/"

lows = ["zprime_m750",       
        "zprime_m1000",      
        "qcd_170_300",
        "qcd_300_470",
    ]
        
highs = [
    "zprime_m1250",      
    "zprime_m2000_low",  
    "zprime_m2000",      
    "zprime_m3000",      
    "qcd_470_600",
#     "qcd_600_800",
    "qcd_800_1000",
    "qcd_1000_1400",]

for name,samples in [ ["low", lows], 
                      ["high", highs]
]:

    #"X_nconst",
    #"X_ncharged",
    #"X_nneutral",

    # Everything that does not need a previous mass cut is a mass (-;
    masses = [#"X_mass",
              #"Xsoftdropz10b00_mass",
              #"Xsoftdropz20b10_mass",
              #"Xsoftdropz20b20_mass",

              "Xsoftdropz10bm10_mass",
              "Xsoftdropz15bm10_mass",
              "Xsoftdropz20bm10_mass",
              
              #"Xtrimmedr2f3_mass",

              #"Xfilteredn3r2_mass",     
              #"Xfilteredn5r2_mass",     
              #"Xprunedn3z10rfac50_mass",

              #"log(X_chi1)",
              #"log(X_chi2)",
              #"log(X_chi3)",

              #"looseOptRHTT_mass",

              #"Xcmstt_minMass",
              #"Xcmstt_topMass",
              #"Xcmstt_nSubJets"
    ]

    

    # These need a cut on the HTT mass
    htt_vars = [
        "looseOptRHTT_fRec",
        "looseOptRHTT_Ropt-looseOptRHTT_RoptCalc",
        ]

    # These need a mass-cut
    others = [
        "X_tau3/X_tau2",
        "X_qvol",        
        "Xsoftdropz10b00forbtag_btag",
        "Xsoftdropz20b10forbtag_btag",
    ]

    for groomer in [#"filteredn3r2",
                    #"prunedn3z10rfac50",
                    #"trimmedr2f3",
                    "softdropz10b00",            
                    "softdropz20b10"
    ]:
        others.append("X{0}_tau3/X{0}_tau2".format(groomer))
        #others.append("X_tau3/X{0}_tau2".format(groomer))
        #others.append("X{0}_tau3/X_tau2".format(groomer))

    if True:
        for var in masses:# + others:

            if name == "high":

                xpos = 0.6
                ypos = 0.6
                ymax = None
                nbins = 80
                extra_text = "AK08, flat pT"

                if "filtered" in var:
                    ymax = 0.2

                if "softdrop" in var and ("b10" in var or "b20" in var):
                    ymax = 0.13

                if "trimmed" in var:
                    ymax = 0.15

                if "chi" in var:                    
                    ymax = 0.12
                    
                if "chi1" in var:
                    extra_text = "AK08, MJ R=0.1, flat pT"
                if "chi2" in var:
                    extra_text = "AK08, MJ R=0.2, flat pT"
                if "chi3" in var:
                    extra_text = "AK08, MJ R=0.3, flat pT"

                if "HTT_mass" in var:
                    xpos = 0.63

                if "HTT" in var:                    
                    extra_text = "CA15, flat pT"

                if "X_tau3/X_tau2" in var:
                    ymax = 0.11

                if "Xsoftdropz10b00_tau3/Xsoftdropz10b00_tau2" in var:
                    ymax = 0.11


            else:
                xpos = 0.6
                ypos = 0.76
                ymax = None
                nbins = 80
                extra_text = "CA15, flat pT"

                if "filtered" in var:
                    ymax = 0.2

                if "chi1" in var:
                    extra_text = "CA15, MJ R=0.1, flat pT"
                if "chi2" in var:
                    extra_text = "CA15, MJ R=0.2, flat pT"
                if "chi3" in var:
                    extra_text = "CA15, MJ R=0.3, flat pT"


                if "softdrop" in var and ("b10" in var or "b20" in var):
                    ymax = 0.13

                if "trimmed" in var:
                    ymax = 0.15

            combinedPlot("fixedMatch_nosize_" + var.replace("/","_")+"_"+name,
                         [plot(other2_sample_names[sample],
                               variable.di[var.replace("X",ranges[sample][4])].name,                                           
                               '({0}&&{1})*weight'.format(nosize_fiducial_cuts[sample], variable.di[var.replace("X",ranges[sample][4])].extra_cut),
                               sample) for sample in samples],
                         80, variable.di[var.replace("X",ranges[sample][4])].range_min, variable.di[var.replace("X",ranges[sample][4])].range_max, ymax,
                         label_x   = variable.di[var.replace("X",ranges[sample][4])].pretty_name,
                         label_y   = "A.U.",
                         axis_unit = variable.di[var.replace("X",ranges[sample][4])].unit,
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = xpos,
                         legend_origin_y = ypos,
                         legend_size_x   = 0.2,
                         legend_text_size= 0.03,
                         extra_text = extra_text)
            
    if False:
        for var in others:

            if name == "high":

                xpos = 0.6
                ypos = 0.6
                ymax = None
                nbins = 80
                extra_text = "AK08, flat pT"
                
                cut = "((ak08softdropz10b00_mass>110)&&(ak08softdropz10b00_mass<210))"

                if "X_tau3/X_tau2" in var:
                    ymax = 0.11

                if "Xsoftdropz10b00_tau3/Xsoftdropz10b00_tau2" in var:
                    ymax = 0.11

                if "HTT" in var:                    
                    extra_text = "CA15, flat pT"

            else:
                xpos = 0.6
                ypos = 0.76
                ymax = None
                nbins = 80
                extra_text = "CA15, flat pT"

                cut = "((ca15softdropz20b10_mass>150)&&(ca15softdropz20b10_mass<240))"


            combinedPlot("fixedMatch_nosize_masscut_" + var.replace("/","_")+"_"+name,
                         [plot(other2_sample_names[sample],
                               variable.di[var.replace("X",ranges[sample][4])].name,                                           
                               '({0}&&{1}&&{2})*weight'.format(nosize_fiducial_cuts[sample], 
                                                               variable.di[var.replace("X",ranges[sample][4])].extra_cut,
                                                               cut),
                               sample) for sample in samples],
                         80, variable.di[var.replace("X",ranges[sample][4])].range_min, variable.di[var.replace("X",ranges[sample][4])].range_max, ymax,
                         label_x   = variable.di[var.replace("X",ranges[sample][4])].pretty_name,
                         label_y   = "A.U.",
                         axis_unit = variable.di[var.replace("X",ranges[sample][4])].unit,
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = xpos,
                         legend_origin_y = ypos,
                         legend_size_x   = 0.2,
                         legend_text_size= 0.03,
                         extra_text = extra_text)
            

    if False:
        for var in htt_vars:

            if name == "high":

                xpos = 0.6
                ypos = 0.6
                ymax = None
                nbins = 80
                extra_text = "AK08, flat pT"

                if "HTT" in var:                    
                    extra_text = "CA15, flat pT"


                cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))"

            else:
                xpos = 0.6
                ypos = 0.76
                ymax = None
                nbins = 80
                extra_text = "CA15, flat pT"
                                
                cut = "((looseOptRHTT_mass>120)&&(looseOptRHTT_mass<180))"


            combinedPlot("fixedMatch_nosize_httmasscut_" + var.replace("/","_")+"_"+name,
                         [plot(other2_sample_names[sample],
                               variable.di[var.replace("X",ranges[sample][4])].name,                                           
                               '({0}&&{1}&&{2})*weight'.format(nosize_fiducial_cuts[sample], 
                                                               variable.di[var.replace("X",ranges[sample][4])].extra_cut,
                                                               cut),
                               sample) for sample in samples],
                         80, variable.di[var.replace("X",ranges[sample][4])].range_min, variable.di[var.replace("X",ranges[sample][4])].range_max, ymax,
                         label_x   = variable.di[var.replace("X",ranges[sample][4])].pretty_name,
                         label_y   = "A.U.",
                         axis_unit = variable.di[var.replace("X",ranges[sample][4])].unit,
                         log_y     = False,
                         normalize = True,
                         legend_origin_x = xpos,
                         legend_origin_y = ypos,
                         legend_size_x   = 0.2,
                         legend_text_size= 0.03,
                         extra_text = extra_text)


doWork(full_file_names, output_dir )




