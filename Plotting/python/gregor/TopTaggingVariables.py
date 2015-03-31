#!/usr/bin/env python
"""
Collection of Top Tagging Variables (so we can use them across Plotting/Correlation/TMVA)
"""

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.VariableHelpers import variable
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.VariableHelpers import variable


variable('top_size', "Top Size", 0, 4.)

#mass_vars_15 = [
#    variable('ca15_mass', "m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15filtered_mass', "filtered m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15pruned_mass', "pruned m (z=0.1, r=0.5, R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15newpruned_mass', "pruned m (z=0.05, r=0.5, R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15trimmed_mass', "trimmed m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdrop_mass', "softdrop m (z=0.1, #beta=0, R=1.5)", 0, 1000, unit = "GeV"),   
#    variable('ca15newsoftdrop_mass', "softdrop m (z=0.15, #beta=2, R=1.5)", 0, 1000, unit = "GeV"),   
#]
#
#new_mass_vars_15 = [
#    variable('ca15trimmedr2f3_mass', "trim r2f3 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15trimmedr2f6_mass', "trim r2f6 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz10b00_mass', "sd 10b00 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz10b10_mass', "sd 10b10 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz10b20_mass', "sd 10b20 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz15b00_mass', "sd 15b00 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz15b10_mass', "sd 15b10 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz15b20_mass', "sd 15b20 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz20b00_mass', "sd 20b00 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz20b10_mass', "sd 20b10 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz20b20_mass', "sd 20b20 m (R=1.5)", 0, 1000, unit = "GeV"),    
#]
#
#mass_vars_15_v21 = [
#    variable('ca15trimmedr2f4_mass', "trim r2f4 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15trimmedr2f6_mass', "trim r2f6 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15trimmedr2f8_mass', "trim r2f8 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz15b00_mass', "sd 15b00 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz20b10_mass', "sd 20b10 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz30b20_mass', "sd 30b20 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz30b30_mass', "sd 30b30 m (R=1.5)", 0, 1000, unit = "GeV"),
#    variable('ca15softdropz30b100_mass', "sd 30b100 m (R=1.5)", 0, 1000, unit = "GeV"),
#]
#
#mass_vars_08_v21 = [
#    variable('ca08trimmedr2f4_mass', "trim r2f4 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08trimmedr2f6_mass', "trim r2f6 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08trimmedr2f8_mass', "trim r2f8 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz15b00_mass', "sd 15b00 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz20b10_mass', "sd 20b10 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz30b20_mass', "sd 30b20 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz30b30_mass', "sd 30b30 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz30b100_mass', "sd 30b100 m (R=0.8)", 0, 1000, unit = "GeV"),
#]
#
## V27
#
#groomers_v27 = [
#    "",
#    "trimmedr2f6",
#    "trimmedr2f10",
#    "softdropz15b00",
#    "softdropz20b10",
#    "softdropz30b10",
#    "softdropz30b15",
#]
#
#
#
#mass_vars_v27 = []
#qvol_vars_v27 = []
#nsub_vars_v27 = []
#cmstt_vars_v27 = []
#
#for fj in ["ca08", 
#           "ca15", 
#           "ca08puppi", 
#           "ca15puppi"]:
#
#    qvol_vars_v27.append(variable(fj+"_qvol", "Q-jet vola.", 0, 1.))
#    for groomer in groomers_v27:
#        mass_vars_v27.append(variable(fj+groomer+"_mass", fj+"_"+groomer, 0, 400, unit = "GeV"))
#        nsub_vars_v27.append(variable("{0}{1}_tau3/{0}{1}_tau2".format(fj,groomer), 
#                                      "#tau_{3}/#tau_{2}", 
#                                      0, 1., 
#                                      extra_cut = "({0}{1}_tau2>0)".format(fj,groomer)))
#
#    cmstt_vars_v27.append(variable(fj+'cmstt_minMass', 
#                                   fj+"cmstt_minMass",  
#                                   0, 400, unit = "GeV", 
#                                   extra_cut = "({0}cmstt_nSubJets >= 3)".format(fj)))
#    cmstt_vars_v27.append(variable(fj+'cmstt_topMass', 
#                                   fj+"cmstt_topMass",  
#                                   0, 800, unit = "GeV",
#                                   extra_cut = "({0}cmstt_nSubJets >= 3)".format(fj)))
#
#
#htt_v27 = ["looseMultiRHTT", "softdropz15b00MultiRHTT", "softdropz20b10MultiRHTT"]
#htt_vars_v27 = []
#for htt in htt_v27:
#    htt_vars_v27.append(variable(htt+'_mass', htt+"_m", 0, 400, unit = "GeV"))
#    htt_vars_v27.append(variable(htt+'_fW', htt+"_fW", 0, 0.8))
#    htt_vars_v27.append(variable('{0}_Rmin-{0}_RminExpected'.format(htt), htt+"_DeltaRmin", -0.8, 1.))
#
#ineresting_lowpt_vars_v27 = [
#    variable.di["ca15trimmedr2f6_mass"],
#    variable.di["ca15puppitrimmedr2f6_mass"],
#    variable.di["ca15softdropz20b10_mass"],
#    variable.di["ca15puppisoftdropz20b10_mass"],
#    variable.di["ca15softdropz30b15_mass"],
#    variable.di["ca15puppisoftdropz30b15_mass"],
#    variable.di["ca15_qvol"],
#    variable.di["ca15puppi_qvol"],
#    variable.di["ca15_tau3/ca15_tau2"],
#    variable.di["ca15puppi_tau3/ca15puppi_tau2"],
#    variable.di["ca15trimmedr2f6_tau3/ca15trimmedr2f6_tau2"],
#    variable.di["ca15puppitrimmedr2f6_tau3/ca15puppitrimmedr2f6_tau2"],
#    variable.di["ca15puppicmstt_minMass"],
#    variable.di["ca15puppicmstt_topMass"],
#]
#
#ineresting_midpt_vars_v27 = [
#    variable.di["ca08trimmedr2f6_mass"],
#    variable.di["ca08puppitrimmedr2f6_mass"],
#    variable.di["ca08softdropz15b00_mass"],
#    variable.di["ca08puppisoftdropz15b00_mass"],
#
#    variable.di["ca08_qvol"],
#    variable.di["ca08puppi_qvol"],
#    variable.di["ca08_tau3/ca08_tau2"],
#    variable.di["ca08puppi_tau3/ca08puppi_tau2"],
#
#    variable.di["ca08cmstt_minMass"],
#    variable.di["ca08cmstt_topMass"],
#    variable.di["ca08puppicmstt_minMass"],
#    variable.di["ca08puppicmstt_topMass"],
#
#]
#
#ineresting_highpt_vars_v27 = [
#    variable.di["ca08trimmedr2f6_mass"],
#    variable.di["ca08puppitrimmedr2f6_mass"],
#    variable.di["ca08softdropz15b00_mass"],
#    variable.di["ca08puppisoftdropz15b00_mass"],
#
#    variable.di["ca08_qvol"],
#    variable.di["ca08puppi_qvol"],
#    variable.di["ca08_tau3/ca08_tau2"],
#    variable.di["ca08puppi_tau3/ca08puppi_tau2"],
#
#    variable.di["ca08cmstt_minMass"],
#    variable.di["ca08cmstt_topMass"],
#    variable.di["ca08puppicmstt_minMass"],
#    variable.di["ca08puppicmstt_topMass"],
#
#]
#
## v36
#
#groomers_v36 = [
#    "",
#    "trimmedr2f3",
#    "trimmedr2f6",
#    "trimmedr2f10",
#    "softdropz10b00",
#    "softdropz15b00",
#    "softdropz15b10",
#    "softdropz15b20",
#    "softdropz20b10",
#    "softdropz30b10",
#    "softdropz30b15",
#]
#
#
#mass_vars_v36 = []
#qvol_vars_v36 = []
#nsub_vars_v36 = []
#cmstt_vars_v36 = []
#
#for fj in ["ca08", 
#           "ca15", 
#           "ca08puppi", 
#           "ca15puppi"]:
#
#    qvol_vars_v36.append(variable(fj+"_qvol", fj+"_qvol", 0, 1.))
#    for groomer in groomers_v36:
#        mass_vars_v36.append(variable(fj+groomer+"_mass", fj+"_"+groomer, 0, 400, unit = "GeV"))
#        nsub_vars_v36.append(variable("{0}{1}_tau3/{0}{1}_tau2".format(fj,groomer), 
#                                      fj+"_"+groomer+"_nsub", 
#                                      0, 1., 
#                                      extra_cut = "({0}{1}_tau2>0)".format(fj,groomer)))
#
#    cmstt_vars_v36.append(variable(fj+'cmstt_minMass', 
#                                   fj+"cmstt_minMass",  
#                                   0, 400, unit = "GeV", 
#                                   extra_cut = "({0}cmstt_nSubJets >= 3)".format(fj)))
#    cmstt_vars_v36.append(variable(fj+'cmstt_topMass', 
#                                   fj+"cmstt_topMass",  
#                                   0, 800, unit = "GeV",
#                                   extra_cut = "({0}cmstt_nSubJets >= 3)".format(fj)))
#
#
#htt_v36 = ["looseMultiRHTT", 
#           "looseMultiRHTTpuppi", 
#           #"softdropz20b10MultiRHTT",
#           #"softdropz15bminus20MultiRHTT",
#           #"softdropz15bminus10MultiRHTT",
#           #"softdropz15b00MultiRHTT",
#           #"softdropz15b10MultiRHTT",
#]
#
#htt_vars_v36 = []
#for htt in htt_v36:
#    htt_vars_v36.append(variable(htt+'_mass', htt+"_m", 0, 400, unit = "GeV"))
#    htt_vars_v36.append(variable(htt+'_fW', htt+"_fW", 0, 0.8))
#    htt_vars_v36.append(variable('{0}_Rmin-{0}_RminExpected'.format(htt), 
#                                 htt+"_DeltaRmin", 
#                                 -0.8, 1., 
#                                 extra_cut = "({0}_mass > 0)".format(htt)
#                             ))
#
#ineresting_lowpt_vars_v36 = [
#    variable.di["ca15trimmedr2f6_mass"],
#    variable.di["ca15puppitrimmedr2f6_mass"],
#    variable.di["ca15softdropz15b10_mass"],
#    variable.di["ca15puppisoftdropz15b10_mass"],
#    variable.di["ca15softdropz30b15_mass"],
#    variable.di["ca15puppisoftdropz30b15_mass"],
#    variable.di["ca15_qvol"],
#    variable.di["ca15puppi_qvol"],
#    variable.di["ca15_tau3/ca15_tau2"],
#    variable.di["ca15puppi_tau3/ca15puppi_tau2"],
#    variable.di["ca15trimmedr2f6_tau3/ca15trimmedr2f6_tau2"],
#    variable.di["ca15puppitrimmedr2f6_tau3/ca15puppitrimmedr2f6_tau2"],
#    variable.di["ca15puppicmstt_minMass"],
#    variable.di["ca15puppicmstt_topMass"],
#    variable.di["looseMultiRHTT_mass"],
#    variable.di["looseMultiRHTT_fW"],
#    variable.di["looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected"],
#]
#
#
#ineresting_midpt_vars_v36 = [
#    variable.di["ca08trimmedr2f6_mass"],
#    variable.di["ca08puppitrimmedr2f6_mass"],
#    variable.di["ca08softdropz15b00_mass"],
#    variable.di["ca08puppisoftdropz15b00_mass"],
#
#    variable.di["ca08_qvol"],
#    variable.di["ca08puppi_qvol"],
#    variable.di["ca08_tau3/ca08_tau2"],
#    variable.di["ca08puppi_tau3/ca08puppi_tau2"],
#
#    variable.di["ca08cmstt_minMass"],
#    variable.di["ca08cmstt_topMass"],
#    variable.di["ca08puppicmstt_minMass"],
#    variable.di["ca08puppicmstt_topMass"],
#
#    variable.di["looseMultiRHTT_mass"],
#    variable.di["looseMultiRHTT_fW"],
#    variable.di["looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected"],
#
#    variable.di["looseMultiRHTTpuppi_mass"],
#    variable.di["looseMultiRHTTpuppi_fW"],
#    variable.di["looseMultiRHTTpuppi_Rmin-looseMultiRHTTpuppi_RminExpected"],
#
#
#]
#
#
#ineresting_highpt_vars_v36 = [
#    variable.di["ca08trimmedr2f6_mass"],
#    variable.di["ca08puppitrimmedr2f6_mass"],
#    variable.di["ca08softdropz15b00_mass"],
#    variable.di["ca08puppisoftdropz15b00_mass"],
#
#    variable.di["ca08_qvol"],
#    variable.di["ca08puppi_qvol"],
#    variable.di["ca08_tau3/ca08_tau2"],
#    variable.di["ca08puppi_tau3/ca08puppi_tau2"],
#
#    variable.di["ca08cmstt_minMass"],
#    variable.di["ca08cmstt_topMass"],
#    variable.di["ca08puppicmstt_minMass"],
#    variable.di["ca08puppicmstt_topMass"],
#
#    variable.di["looseMultiRHTT_mass"],
#    variable.di["looseMultiRHTT_fW"],
#    variable.di["looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected"],
#
#    variable.di["looseMultiRHTTpuppi_mass"],
#    variable.di["looseMultiRHTTpuppi_fW"],
#    variable.di["looseMultiRHTTpuppi_Rmin-looseMultiRHTTpuppi_RminExpected"],
#
#
#]
#
#
#
#ineresting_lowpt_vars_v37 = [
#
#    variable('ca15trimmedr2f6forbtag_btag', 
#             'ca15trimmedr2f6forbtag_btag', 
#             0, 1, unit = ""),
#    variable.di["ca15trimmedr2f6_mass"],
#    variable.di["ca15puppitrimmedr2f6_mass"],
#    variable.di["ca15softdropz15b10_mass"],
#    variable.di["ca15puppisoftdropz15b10_mass"],
#    variable.di["ca15softdropz30b15_mass"],
#    variable.di["ca15puppisoftdropz30b15_mass"],
#    variable.di["ca15_qvol"],
#    variable.di["ca15puppi_qvol"],
#    variable.di["ca15_tau3/ca15_tau2"],
#    variable.di["ca15puppi_tau3/ca15puppi_tau2"],
#    variable.di["ca15trimmedr2f6_tau3/ca15trimmedr2f6_tau2"],
#    variable.di["ca15puppitrimmedr2f6_tau3/ca15puppitrimmedr2f6_tau2"],
#    variable.di["ca15puppicmstt_minMass"],
#    variable.di["ca15puppicmstt_topMass"],
#    variable.di["looseMultiRHTT_mass"],
#    variable.di["looseMultiRHTT_fW"],
#    variable.di["looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected"],
#]
#

htt_v39 = ["looseOptRHTT"]# "looseOptRQHTT", "tightOptRQHTT"]



htt_vars_v39 = []
for htt in htt_v39:
    htt_vars_v39.append(variable(htt+'_mass', "mass", 0, 400, unit = "GeV"))
    htt_vars_v39.append(variable(htt+'_fRec', "f_{Rec}", 0, 0.8))
    htt_vars_v39.append(variable('{0}_Ropt-{0}_RoptCalc'.format(htt), 
                                 "#Delta R_{opt}", 
                                 -0.8, 1., 
                                 extra_cut = "({0}_mass > 0)".format(htt)
                             ))
#    htt_vars_v39.append(variable("{0}_tau3unfilt/{0}_tau2unfilt".format(htt), 
#                                 htt+"_nsubunfilt", 
#                                 0, 1,
#                                 extra_cut = "{0}_tau2unfilt>0".format(htt)))
#    htt_vars_v39.append(variable("{0}_tau3filt/{0}_tau2filt".format(htt), 
#                                 htt+"_nsubfilt", 
#                                 0, 1,
#                                 extra_cut = "{0}_tau2filt>0".format(htt)))
#
#    if "QHTT" in htt:
#            htt_vars_v39.append(variable("log("+htt+'_qweight)', htt+"_qweight", -100, 0))
#            htt_vars_v39.append(variable(htt+'_qepsilon', htt+"_qepsilom", 0, 1.6))
#            htt_vars_v39.append(variable(htt+'_qsigmam', htt+"_sigmam", 0, 10,   extra_cut = "({0}_mass > 0)".format(htt)))
#


groomers_v39 = [
    "",
    "trimmedr2f6",
    "softdropz10b00",
    "softdropz15b00",
    "softdropz15b10",
    "softdropz15b20",
    "softdropz20b10",
    "softdropz30b10",
    "softdropz30b15",
]

groomer_names_v39 = [
    "Ungroomed",
    "Trimmed (r=0.2, f=0.06)",
    "Softdrop (z=0.1, #beta=0)",
    "Softdrop (z=0.15, #beta=0)",
    "Softdrop (z=0.15, #beta=1)",
    "Softdrop (z=0.15, #beta=2)",
    "Softdrop (z=0.2, #beta=1)",
    "Softdrop (z=0.3, #beta=1)",
    "Softdrop (z=0.3, #beta=1.5)",
]


mass_vars_v39 = []
cmstt_vars_v40 = []

for fj in ["ca08", 
           "ca15", 
           "ca08puppi", 
           "ca15puppi"
]:

    for groomer, groomer_name in zip(groomers_v39, groomer_names_v39):
        mass_vars_v39.append(variable(fj+groomer+"_mass", groomer_name, 0, 400, unit = "GeV"))
        

    cmstt_vars_v40.append(variable(fj+'cmstt_minMass', 
                                   "min. Mass",  
                                   0, 400, unit = "GeV", 
                                   extra_cut = "({0}cmstt_nSubJets >= 3)".format(fj)))
    cmstt_vars_v40.append(variable(fj+'cmstt_topMass', 
                                   "top Mass",  
                                   0, 800, unit = "GeV",
                                   extra_cut = "({0}cmstt_nSubJets >= 3)".format(fj)))

    variable("{0}_tau3/{0}_tau2".format(fj), 
             "#tau_{3}/#tau_{2}", 
             0, 1., 
             extra_cut = "({0}_tau2>0)".format(fj)),
    
    variable("{0}_qvol".format(fj), 
             "Q-jet volatility", 
             0, 1.5),


mass_vars_v40 = mass_vars_v39
htt_vars_v40 = htt_vars_v39

variable('ca15trimmedr2f6forbtag_btag', "btag", 0, 1.)
variable('ca08trimmedr2f6forbtag_btag', "btag", 0, 1.)



interesting_vars_v40 = { "ca15" : [variable.di['ca15_mass'],
                                   variable.di['ca15trimmedr2f6_mass'],
                                   variable.di['ca15softdropz10b00_mass'],
                                   variable.di['ca15softdropz15b20_mass'],
                                   variable.di['ca15_tau3/ca15_tau2'],
                                   variable.di['ca15_qvol'],
                                   #variable.di['ca15trimmedr2f6forbtag_btag']
                               ],
                         "ca08" : [variable.di['ca08_mass'],
                                   variable.di['ca08trimmedr2f6_mass'],
                                   variable.di['ca08softdropz10b00_mass'],
                                   variable.di['ca08softdropz15b20_mass'],
                                   variable.di['ca08_tau3/ca08_tau2'],
                                   variable.di['ca08_qvol'],
                                   #variable.di['ca08trimmedr2f6forbtag_btag']
                               ]
}

interesting_puppi_vars_v40 = { "ca15" : [variable.di['ca15puppi_mass'],
                                   variable.di['ca15puppitrimmedr2f6_mass'],
                                   variable.di['ca15puppisoftdropz10b00_mass'],
                                   variable.di['ca15puppisoftdropz15b20_mass'],
                                   variable.di['ca15puppi_tau3/ca15puppi_tau2'],
                                   variable.di['ca15puppi_qvol'],
                                   #variable.di['ca15trimmedr2f6forbtag_btag']
                               ],
                         "ca08" : [variable.di['ca08puppi_mass'],
                                   variable.di['ca08puppitrimmedr2f6_mass'],
                                   variable.di['ca08puppisoftdropz10b00_mass'],
                                   variable.di['ca08puppisoftdropz15b20_mass'],
                                   variable.di['ca08puppi_tau3/ca08puppi_tau2'],
                                   variable.di['ca08puppi_qvol'],
                                   #variable.di['ca08trimmedr2f6forbtag_btag']
                               ]
}


variable('log(ca15_chi)', "log(#chi)", -10., 10, extra_cut = 'ca15_chi>0')
variable('log(ca08_chi)', "log(#chi)", -10., 10, extra_cut = 'ca08_chi>0')



#mass_vars_08 = [
#    variable('ca08_mass', "m (R=0.8)", 0, 500, unit = "GeV"),
#    variable('ca08filtered_mass', "filtered m (R=0.8)", 0, 500, unit = "GeV"),
#    variable('ca08pruned_mass', "pruned m (z=0.1, r=0.5, R=0.8)", 0, 500, unit = "GeV"),
#    variable('ca08newpruned_mass', "pruned m (z=0.05, r=0.5, R=0.8)", 0, 500, unit = "GeV"),
#    variable('ca08trimmed_mass', "trimmed m (R=0.8)", 0, 500, unit = "GeV"),
#    variable('ca08softdrop_mass', "softdrop m (z=0.1, #beta=0, R=0.8)", 0, 500, unit = "GeV"),   
#    variable('ca08newsoftdrop_mass', "softdrop m (z=0.15, #beta=2, R=0.8)", 0, 500, unit = "GeV"),   
#]
#
#new_mass_vars_08 = [
#    variable('ca08trimmedr2f3_mass', "trim r2f3 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08trimmedr2f6_mass', "trim r2f6 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz10b00_mass', "sd 10b00 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz10b10_mass', "sd 10b10 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz10b20_mass', "sd 10b20 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz15b00_mass', "sd 15b00 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz15b10_mass', "sd 15b10 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz15b20_mass', "sd 15b20 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz20b00_mass', "sd 20b00 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz20b10_mass', "sd 20b10 m (R=0.8)", 0, 1000, unit = "GeV"),
#    variable('ca08softdropz20b20_mass', "sd 20b20 m (R=0.8)", 0, 1000, unit = "GeV"),    
#]
#
#
#tau_vars_15 = [
#    variable('ca15_tau3/ca15_tau2', "#tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
#    variable('ca15filtered_tau3/ca15filtered_tau2', "filtered #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
#    variable('ca15pruned_tau3/ca15pruned_tau2', "pruned #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
#    variable('ca15newpruned_tau3/ca15newpruned_tau2', "newpruned #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
#    variable('ca15trimmed_tau3/ca15trimmed_tau2', "trimmed #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),
#    variable('ca15softdrop_tau3/ca15softdrop_tau2', "softdrop #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),    
#    variable('ca15newsoftdrop_tau3/ca15newsoftdrop_tau2', "newsoftdrop #tau_{3}/#tau_{2}  (R=1.5)", 0, 1.),    
#]
#
#tau_vars_08 = [
#    variable('ca08_tau3/ca08_tau2', "#tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
#    variable('ca08filtered_tau3/ca08filtered_tau2', "filtered #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
#    variable('ca08pruned_tau3/ca08pruned_tau2', "pruned #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
#    variable('ca08newpruned_tau3/ca08newpruned_tau2', "newpruned #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
#    variable('ca08trimmed_tau3/ca08trimmed_tau2', "trimmed #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),
#    variable('ca08softdrop_tau3/ca08softdrop_tau2', "softdrop #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),    
#    #variable('ca08softdrop_tau3/ca08_tau2', "#tau_{3, softdrop}/#tau_{2}  (R=0.8)", 0.01, 1.),
#    #variable('ca08_tau3/ca08softdrop_tau2', "#tau_{3}/#tau_{2,softdrop}  (R=0.8)", 0.01, 1.),
#    variable('ca08newsoftdrop_tau3/ca08newsoftdrop_tau2', "newsoftdrop #tau_{3}/#tau_{2}  (R=0.8)", 0.01, 1.),    
#    #variable('ca08newsoftdrop_tau3/ca08_tau2', "#tau_{3, newsoftdrop}/#tau_{2}  (R=0.8)", 0.01, 1.),
#    #variable('ca08_tau3/ca08newsoftdrop_tau2', "#tau_{3}/#tau_{2,newsoftdrop}  (R=0.8)", 0.01, 1.),
#]
#
#tau31_vars_15 = [
#    variable('ca15_tau3/ca15_tau1', "#tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),
#    variable('ca15filtered_tau3/ca15filtered_tau1', "filtered #tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),
#    variable('ca15pruned_tau3/ca15pruned_tau1', "pruned #tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),
#    variable('ca15trimmed_tau3/ca15trimmed_tau1', "trimmed #tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),
#    variable('ca15softdrop_tau3/ca15softdrop_tau1', "softdrop #tau_{3}/#tau_{1}  (R=1.5)", 0, 1.),    
#]
#
#tau31_vars_08 = [
#    variable('ca08_tau3/ca08_tau1', "#tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),
#    variable('ca08filtered_tau3/ca08filtered_tau1', "filtered #tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),
#    variable('ca08pruned_tau3/ca08pruned_tau1', "pruned #tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),
#    variable('ca08trimmed_tau3/ca08trimmed_tau1', "trimmed #tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),
#    variable('ca08softdrop_tau3/ca08softdrop_tau1', "softdrop #tau_{3}/#tau_{1}  (R=0.8)", 0.01, 1.),    
#]
#
#
#
#
#btag_vars = [
#    variable('ca15_btag', "btag (R=1.5)", -0.1, 1.1),
#    variable('ca08_btag', "btag (R=0.8)", -0.1, 1.1),
#]
#
#
#htt_vars = [
#    variable('looseMultiRHTT_mass', "HTT m", 0, 400, unit = "GeV"),
#    variable('looseMultiRHTT_fW', "HTT f_{W}", 0, 0.8),
#    variable('looseMultiRHTT_Rmin-looseMultiRHTT_RminExpected', "HTT #Delta R_{min,exp}", -0.8, 1., extra_cut = "looseMultiRHTT_mass>0"),
#    variable('looseMultiRHTT_Rmin-(-0.2695+0.0154709*sqrt(looseMultiRHTT_ptFiltForRminExp)+321.749/looseMultiRHTT_ptFiltForRminExp+42234.2/(looseMultiRHTT_ptFiltForRminExp*looseMultiRHTT_ptFiltForRminExp)+-1.2832e+07/(looseMultiRHTT_ptFiltForRminExp*looseMultiRHTT_ptFiltForRminExp*looseMultiRHTT_ptFiltForRminExp))', "HTT new delta",-.8,1.)
#]
#
#tagger_vars_15 = [variable('log(ca15_chi)', "log(#chi) (R=1.5)", -10., 10, extra_cut = 'ca15_chi>0'),
#                  variable('ca15_qvol', "Q-Jet Volatility (R=1.5)", 0., 2.5),
#                  variable('ca15cmstt_minMass', "CMSTT minMass (R=1.5)", 0., 400, unit = "GeV"),
#                  variable('ca15cmstt_topMass', "CMSTT topMass (R=1.5)", 0., 600, unit = "GeV")
#              ] + htt_vars 
#                             
#tagger_vars_08 = [
#    variable('log(ca08_chi)', "log(#chi) (R=0.8)", -10., 10, extra_cut = 'ca08_chi>0'),
#    variable('ca08_qvol', "Q-Jet Volatility (R=0.8)", 0., 2.5),
#    variable('ca08cmstt_minMass', "CMSTT minMass (R=0.8)", 0., 250, unit = "GeV"),
#    variable('ca08cmstt_topMass', "CMSTT topMass (R=0.8)", 0., 600., unit = "GeV"),
#]
#
#tagger_vars = tagger_vars_08 + tagger_vars_15
#
#good_vars = [ 
#    #variable.di['ca08softdrop_mass'],
#    #variable.di['ca08_tau3/ca08_tau2'],
#    #variable.di['looseMultiRHTT_mass'],
#    #variable.di['ca08cmstt_minMass'],
#    #              variable.di['ca08_btag'],
#    #              variable.di['log(ca15_chi)'],
#]
#
#
## No good tau=0.8 or masses 0.8 variable
## R=0.8 Combination of tau3newsoftdrop/tau2 and tau3softdrop/tau2 could be fin to try
##
#
#interesting_vars_200_300 = [ 
#    variable.di['ca15filtered_mass'],
#    variable.di['ca15trimmed_mass'],
#    variable.di['ca15newsoftdrop_mass'],
#    variable.di['ca15_tau3/ca15_tau2'],
#    variable.di['ca15filtered_tau3/ca15filtered_tau2'],
#    variable.di['ca15trimmed_tau3/ca15trimmed_tau2'],
#    variable.di['ca15_qvol'],
#
#]
#
#good_vars_200_300 = [ 
#    variable.di['ca15trimmed_mass'],
#    variable.di['ca15filtered_mass'],
#    variable.di['ca15newsoftdrop_mass'],
#    variable.di['log(ca15_chi)'],
#]
#
#
#interesting_vars_470_600 = [ 
#    variable.di['ca08trimmed_mass'],
#    variable.di['ca08pruned_mass'],
#    variable.di['ca08newsoftdrop_mass'],
#    variable.di['ca08_tau3/ca08_tau2'],
#    variable.di['ca08_qvol'],
#]
#
#good_vars_470_600 = [ 
#    variable.di['ca08trimmed_mass'],
##    variable.di['ca08pruned_mass'],
#    variable.di['ca08newsoftdrop_mass'],
#    variable.di['log(ca15_chi)'],
#]
#
#interesting_vars_800_1000 = [ 
#    variable.di['ca08trimmed_mass'],
#    variable.di['ca08softdrop_mass'],
#    variable.di['ca08pruned_mass'],
#    variable.di['ca08_tau3/ca08_tau2'],
#    variable.di['ca08_qvol'],
#]
#
#good_vars_800_1000 = [ 
#    variable.di['ca08trimmed_mass'],
#    variable.di['ca08softdrop_mass'],
#    variable.di['ca08pruned_mass'],
#    variable.di['log(ca15_chi)'],
#]
#
#cmstt_vars = [variable.di['ca08cmstt_topMass'],              
#              variable.di['ca08cmstt_minMass'],
#              variable.di['ca15cmstt_topMass'],              
#              variable.di['ca15cmstt_minMass']
#]
#
#
#sd_vars =[]              
#for fj in ["ca08", "ca15", "ca08puppi", "ca15puppi"]:
#    sd_vars.append(variable('log({0}_chi)'.format(fj), "log(#chi)_"+fj, -10., 10, extra_cut = '{0}_chi>0'.format(fj)))
#    sd_vars.append(variable('{0}_nmj'.format(fj), "N (microjets)", 0., 20., extra_cut = '{0}_chi>0'.format(fj)))
#
#
#all_vars_15 = mass_vars_15 + tau_vars_15 +   tagger_vars_15 
#all_vars_08 = mass_vars_08 + tau_vars_08 +   tagger_vars_08
#
#all_vars = all_vars_08 + all_vars_15
