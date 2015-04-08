
#!/usr/bin/env python
"""
Collection of Higgs Tagging Variables (so we can use them across Plotting/Correlation/TMVA)
"""

import os

# With CMSSW
if "CMSSW_VERSION" in os.environ.keys():
    from TTH.Plotting.Helpers.VariableHelpers import variable
# Without CMSSW
else:
    from TTH.Plotting.python.Helpers.VariableHelpers import variable

#
#prettier_names = {'ca15': "Ungroomed",
#                  'ca15filteredn2r2': "Filter(n=2, R=0.2)",
#                  'ca15filteredn2r3': "Filter(n=2, R=0.3)",
#                  'ca15filteredn3r3': "Filter(n=3, R=0.3)",
#                  'ca15filteredn4r2': "Filter(n=4, R=0.2)",
#                  'ca15massdrop': "MD",
#                  'ca15massdropfilteredn2r2': "MD + Filter(n=2, R=0.2)",
#                  'ca15massdropfilteredn2r3': "MD + Filter(n=2, R=0.3)",
#                  'ca15massdropfilteredn3r3': "MD + Filter(n=3, R=0.3)",
#                  'ca15massdropfilteredn4r2': "MD + Filter(n=4, R=0.2)",
#                  'ca15prunedz1r5': "Pruner(z=0.1, r=0.5)",
#                  'ca15prunedz2r5': "Pruner(z=0.2, r=0.5)",
#                  'ca15prunedz1r3': "Pruner(z=0.1, r=0.3)",
#                  'ca15trimmedr2f6': "Trimmer(r=0.2, f=0.06)",
#                  'ca15trimmedr2f3': "Trimmer(r=0.2, f=0.03)",
#                  'ca15trimmedr2f1': "Trimmer(r=0.2, f=0.01)",
#                  'ca15softdropz15b2': "Softdrop(z=0.15, #beta=2)",
#                  'ca15softdropz10b0': "Softdrop(z=0.1, #beta=0)",
#                  'ca15softdropz5b0':  "Softdrop(z=0.05, #beta=0)",
#}
#
#
#
#li_fjs = ['ca15',
#          'ca15filteredn2r2',
#          'ca15filteredn2r3',
#          'ca15filteredn3r3',
#          'ca15filteredn4r2',
#          'ca15massdrop',
#          'ca15massdropfilteredn2r2',
#          'ca15massdropfilteredn2r3',
#          'ca15massdropfilteredn3r3',
#          'ca15massdropfilteredn4r2',
#          'ca15prunedz1r5',
#          'ca15prunedz2r5',
#          'ca15prunedz1r3',
#          'ca15trimmedr2f3',
#          'ca15trimmedr2f1',
#          'ca15trimmedr2f6',
#          'ca15softdropz10b0',
#          'ca15softdropz5b0',
#          'ca15softdropz15b2']
#
#
#mass_vars = [ variable(fj+"_mass", fj, 0, 800, unit = "GeV") for fj in li_fjs   ]
#tau_vars = [ variable("{0}_tau2/{0}_tau1".format(fj), fj + "tau_{2}/tau_{1}", 0., 1., extra_cut = "{0}_tau1>0".format(fj)) for fj in li_fjs   ]
#
#variable.di['ca15_mass'].pretty_name = "Ungroomed mass"
#
#mass_vars_v5 = [
#    variable('ca15trimmedr2f4_mass', "trim r2f4 m (R=1.5)", 0, 800, unit = "GeV"),
#    variable('ca15trimmedr2f6_mass', "Trimmed (r=0.2, f=0.06) mass", 0, 800, unit = "GeV"),
#    variable('ca15trimmedr2f8_mass', "trim r2f8 m (R=1.5)", 0, 800, unit = "GeV"),
#    variable('ca15softdropz15b00_mass', "sd 15b00 m (R=1.5)", 0, 800, unit = "GeV"),
#    variable('ca15softdropz20b10_mass', "Softdrop (z=0.2, #beta=1) mass", 0, 800, unit = "GeV"),
#    variable('ca15softdropz30b20_mass', "sd 30b20 m (R=1.5)", 0, 800, unit = "GeV"),
#    variable('ca15softdropz30b30_mass', "sd 30b30 m (R=1.5)", 0, 800, unit = "GeV"),
#    variable('ca15softdropz30b100_mass', "sd 30b100 m (R=1.5)", 0, 800, unit = "GeV"),
#]
#
#groomers_v7  = ['ca15',
#                'ca15filteredn3r3',
#                'ca15filteredn3r2',
#                'ca15filteredn2r3',
#                'ca15filteredn2r2',
#                'ca15prunedn2z10rfac50',
#                'ca15trimmedr2f3',
#                'ca15trimmedr2f6',
#                'ca15trimmedr2f9',
#                'ca15softdropz10b00',
#                'ca15softdropz15b00',
#                'ca15softdropz15b10',
#                'ca15softdropz20b10',
#                'ca15softdropz30b20',
#                'ca15softdropz30b10',
#                'ca15softdropz30b30',
#                'ca15massdrop',
#                'ca15massdropfiltered'
#]
#
#mass_vars_v7 = [variable(x + '_mass', x +"m", 0, 800, unit = "GeV") for x in groomers_v7]
#
#interesting_vars_v7 = [
#    variable.di['ca15_mass'],
#    variable.di['ca15filteredn3r2_mass'],
#    variable.di['ca15prunedn2z10rfac50_mass'],
#    variable.di['ca15trimmedr2f6_mass'],
#    variable.di['ca15softdropz15b10_mass'],
#    variable.di['ca15massdropfiltered_mass'],
#
#    variable('ca15_tau2/ca15_tau1', "ca15_nsub", 0, 1),
#    variable('ca15_qvol', "ca15_qvol", 0, 1),
#
#]
#

qvol_vars = []
for fj in ["ca15", "ak08"]:
    for qvol in ["QVol0", "QVol0p01", "QVol0p1", "QVol1", "QVol100"]:
        qvol_vars.append(variable("{0}{1}_qvol".format(fj,qvol), "{0}_{1}".format(fj, qvol), 0, 1.))


nice_names = {    
    "ca15": "CA (R=1.5)",
    "ak08": "AK (R=0.8)",
    
    ''             : "Ungroomed", 
    'filteredn3r3' : "Filtered (n=3, r=0.3)",
    'filteredn3r2' : "Filtered (n=3, r=0.2)",
    'filteredn2r3' : "Filtered (n=2, r=0.3)",
    'filteredn2r2' : "Filtered (n=2, r=0.2)",
    'prunedn2z10rfac50' : "Pruned (n=2, z=0.1, rfrac=0.5)",
    'trimmedr2f3' : "Trimmed (r=0.2, f=0.03)",
    'trimmedr2f6' : "Trimmed (r=0.2, f=0.06)",
    'trimmedr2f10' : "Trimmed (r=0.2, f=0.1)",
    'softdropz10b00' : "Softdrop (z=0.1, b=0)",
    'softdropz15b00' : "Softdrop (z=0.15, b=0)",
    'softdropz15b10' : "Softdrop (z=0.15, b=1)",
    'softdropz20b10' : "Softdrop (z=0.2, b=1)",
    'softdropz30b10' : "Softdrop (z=0.3, b=1)",
    'softdropz30b15' : "Softdrop (z=0.3, b=1.5)",
}



mass_vars_v10 = []
for fj in ["ca15","ak08"]:
    for groomer in ["",
                    'filteredn3r3',
                    'filteredn3r2',
                    'filteredn2r3',
                    'filteredn2r2',
                    'prunedn2z10rfac50',
                    'trimmedr2f3',
                    'trimmedr2f6',
                    'trimmedr2f10',
                    'softdropz10b00',
                    'softdropz15b00',
                    'softdropz15b10',
                    'softdropz20b10',
                    'softdropz30b10',
                    'softdropz30b15',
    ]:        
        mass_vars_v10.append(variable("{0}{1}_mass".format(fj,groomer), 
                                      "{0} {1}".format(nice_names[fj], nice_names[groomer]),
                                      0, 300))
mass_vars_ca15_v10 = [x for x in mass_vars_v10 if "ca15" in x.name]
mass_vars_ak08_v10 = [x for x in mass_vars_v10 if "ak08" in x.name]



#
#other_vars = [ variable("ca15_qvol", "q-vol", 0, 1.)]
#
#interesting_vars=[    
#    variable.di['ca15trimmedr2f3_mass'],
#    variable.di['ca15trimmedr2f6_mass'],
#    variable.di['ca15massdropfilteredn4r2_mass'],
#    variable.di['ca15softdropz15b2_mass'],
#    variable.di['ca15_tau2/ca15_tau1'],
# #   variable.di['ca15_qvol'],
#]
#
#interesting_vars_v5 = [    
#    variable.di['ca15trimmedr2f6_mass'],
#    variable.di['ca15softdropz20b10_mass'],
#    variable.di['ca15_tau2/ca15_tau1'],
#    variable.di['ca15_qvol'],
#]
#
#
#
#
##    variable('ca15_mass', "m", 0, 800, unit = "GeV"),
##    variable('ca15filtered_mass', "filtered m", 0, 800, unit = "GeV"),
##    variable('ca15massdrop_mass', "massdrop m", 0, 800, unit = "GeV"),
##    variable('ca15massdropfiltered_mass', "massdrop+filtered m", 0, 800, unit = "GeV"),
##    variable('ca15pruned_mass', "pruned m", 0, 800, unit = "GeV"),
##    variable('ca15trimmed_mass', "trimmed m", 0, 800, unit = "GeV"),
##    variable('ca15softdrop_mass', "softdrop m", 0, 800, unit = "GeV"),   
#
#
##tau_vars = [
###    variable('ca15_tau2/ca15_tau1', "tau_{2}/tau_{1}", 0, 1, unit = ""),
###    variable('ca15filtered_tau2/ca15filtered_tau1', "filtered tau_{2}/tau_{1}", 0, 1, unit = ""),
###    variable('ca15massdrop_tau2/ca15massdrop_tau1', "massdrop tau_{2}/tau_{1}", 0, 1, unit = ""),
###    variable('ca15massdropfiltered_tau2/ca15massdropfiltered_tau1', "massdrop+filtered tau_{2}/tau_{1}", 0, 1, unit = ""),
###    variable('ca15pruned_tau2/ca15pruned_tau1', "pruned tau_{2}/tau_{1}", 0, 1, unit = ""),
###    variable('ca15trimmed_tau2/ca15trimmed_tau1', "trimmed tau_{2}/tau_{1}", 0, 1, unit = ""),
###    variable('ca15softdrop_tau2/ca15softdrop_tau1', "softdrop tau_{2}/tau_{1}", 0, 1, unit = ""),   
##]
##
#btag_vars = [
#    variable('ca15_btag', "btag", 0, 1, unit = "")
#
#]
#
#
#good_vars = [
#    variable.di['ca15_mass'],
#    variable.di['ca15trimmedr2f6_mass'],
#    variable.di['ca15trimmedr2f3_mass'],
#    variable.di['ca15filteredn4r2_mass'],
#    variable.di['ca15massdropfilteredn4r2_mass'],
#    variable.di['ca15massdropfilteredn2r3_mass'],
#    variable.di['ca15prunedz2r5_mass'],
#    variable.di['ca15softdropz15b2_mass'],
#
##    variable.di["ca15trimmed_mass"],
##    variable.di["ca15_tau2/ca15_tau1"],
##    variable.di["ca15_btag"],
#]
#
#all_vars = mass_vars + tau_vars + btag_vars
