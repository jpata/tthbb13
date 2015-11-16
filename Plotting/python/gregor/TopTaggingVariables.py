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


htts = ["looseOptRHTT", "looseHTT", "msortHTT"]
htt_names = ["HTT V2", "HTT V2", "HTT"]

htt_vars = []
for htt, htt_name in zip(htts, htt_names):
    htt_vars.append(variable(htt+'_mass', htt_name+ " Mass", 0, 280, unit = "GeV"))
    htt_vars.append(variable(htt+'_fRec', htt_name+ " f_{Rec}", 0, 0.5))
    htt_vars.append(variable('{0}_Ropt-{0}_RoptCalc'.format(htt), 
                             htt_name + " #Delta R_{opt}", 
                             -0.8, 1., 
                             extra_cut = "({0}_mass > 0)".format(htt)
                         ))

groomers = [
    "",
    "filteredn3r2",
    "filteredn5r2",
    "prunedn3z10rfac50",
    "trimmedr2f3",
    "trimmedr2f6",
    "trimmedr2f9",
    "softdropz10b00",
    "softdropz10b10",
    "softdropz10b20",
    "softdropz15b00",
    "softdropz15b10",
    "softdropz15b20",
    "sofbtdropz20b00",
    "softdropz20b10",
    "softdropz20b20",
    
    "softdropz10bm10",
    "softdropz15bm10",
    "softdropz20bm10",

]

groomer_names = [
    "Ungroomed",
    "Filtered (r=0.2, n=3)",
    "Filtered (r=0.2, n=5)",
    "Pruned (z=0.1, rcut=0.5)",
    "Trimmed (r=0.2, f=0.03)",
    "Trimmed (r=0.2, f=0.06)",
    "Trimmed (r=0.2, f=0.09)",
    "Softdrop (z=0.1, #beta=0)",
    "Softdrop (z=0.1, #beta=1)",
    "Softdrop (z=0.1, #beta=2)",
    "Softdrop (z=0.15, #beta=0)",
    "Softdrop (z=0.15, #beta=1)",
    "Softdrop (z=0.15, #beta=2)",
    "Softdrop (z=0.2, #beta=0)",
    "Softdrop (z=0.2, #beta=1)",
    "Softdrop (z=0.2, #beta=2)",
    "Softdrop (z=0.1, #beta=-1)",
    "Softdrop (z=0.15, #beta=-1)",
    "Softdrop (z=0.2, #beta=-1)",
]


mass_vars = []
cmstt_vars = []

for fj in ["ak08", "ca15"]:

    cmstt_vars.append(variable(fj+'_nconst', 
                                   "Total Number of Constituents",  
                                   -0.5, 319.5))

    cmstt_vars.append(variable(fj+'_ncharged', 
                                   "Number of Charged Constituents",  
                                   -0.5,159.5))

    cmstt_vars.append(variable(fj+'_nneutral', 
                                   "Number of Neutral Constituents",  
                                   -0.5,159.5))


    for groomer, groomer_name in zip(groomers, groomer_names):
        mass_limit = 400
        min_mass   = 0

        if groomer == "":
            mass_limit = 500
        elif "trimmed" in groomer:
            mass_limit = 280
        elif "filtered" in groomer:
            mass_limit = 280
        elif "pruned" in groomer:
            mass_limit = 280
        elif "softdrop" in groomer:
            mass_limit = 280
            
            # Extra treatment for negative beta
            if "m10" in groomer:
                min_mass = 1
                mass_limit = 400
            
            

        mass_vars.append(variable(fj+groomer+"_mass", groomer_name + " Mass", min_mass, mass_limit, unit = "GeV"))
        
        variable("{0}_tau3/{0}{1}_tau2".format(fj, groomer), 
                 groomer_name + "(u/g) #tau_{3}/#tau_{2}", 
                 0, 2., 
                 extra_cut = "({0}{1}_tau2>0)&&({0}_tau2>0)".format(fj,groomer))

        variable("{0}{1}_tau3/{0}_tau2".format(fj, groomer), 
                 groomer_name + "(g/u) #tau_{3}/#tau_{2}", 
                 0, 1., 
                 extra_cut = "({0}_tau2>0)".format(fj))
        
        variable("{0}{1}_tau3/{0}{1}_tau2".format(fj, groomer), 
                 groomer_name + " #tau_{3}/#tau_{2}", 
                 0, 1., 
                 extra_cut = "({0}{1}_tau2>0)".format(fj,groomer))


        
    cmstt_vars.append(variable(fj+'cmstt_nSubJets', 
                                   "CMSTT number of Subjets",  
                                   0.5, 5.5))

    cmstt_vars.append(variable(fj+'cmstt_minMass', 
                                   "CMSTT min. Mass",  
                                   0, 250, unit = "GeV", 
                                   extra_cut = "({0}cmstt_nSubJets >= 3)".format(fj)))

    cmstt_vars.append(variable(fj+'cmstt_topMass', 
                                   "CMSTT top Mass",  
                                   0, 400, unit = "GeV",
                                   extra_cut = "({0}cmstt_nSubJets >= 3)".format(fj)))


    
    variable("{0}_qvol".format(fj), "Q-jet volatility", 0, .5)

variable('ak08trimmedr2f6forbtag_btag', "btag", 0, 1.)


variable('ca15trimmedr2f6forbtag_btag', "Trimmed (r=0.2, f=0.06) btag", 0, 1.)
variable('ca15trimmedr2f3forbtag_btag', "Trimmed (r=0.2, f=0.03) btag", 0, 1.)
variable('ca15softdropz10b00forbtag_btag', "Softdrop (z=0.1, #beta=0) btag", 0, 1.)
variable('ca15softdropz20b10forbtag_btag', "Softdrop (z=0.2, #beta=1) btag", 0, 1.)
variable('ca15filteredn3r2forbtag_btag', "Filtered btag", 0, 1.)
variable('ca15prunedn3z10rfac50forbtag_btag', "Pruned btag", 0, 1.)

variable('ak08trimmedr2f6forbtag_btag', "Trimmed (r=0.2, f=0.06) btag", 0, 1.)
variable('ak08trimmedr2f3forbtag_btag', "Trimmed (r=0.2, f=0.03) btag", 0, 1.)
variable('ak08softdropz10b00forbtag_btag', "Softdrop (z=0.1, #beta=0) btag", 0, 1.)
variable('ak08softdropz20b10forbtag_btag', "Softdrop (z=0.2, #beta=1) btag", 0, 1.)
variable('ak08filteredn3r2forbtag_btag', "Filtered btag", 0, 1.)
variable('ak08prunedn3z10rfac50forbtag_btag', "Pruned btag", 0, 1.)



variable('log(ak08_chi1)', "log(#chi) (R=0.1)", -10., 10, extra_cut = 'ak08_chi1>0')
variable('log(ca15_chi1)', "log(#chi) (R=0.1)", -10., 10, extra_cut = 'ca15_chi1>0')

variable('log(ak08_chi2)', "log(#chi) (R=0.2)", -10., 10, extra_cut = 'ak08_chi2>0')
variable('log(ca15_chi2)', "log(#chi) (R=0.2)", -10., 10, extra_cut = 'ca15_chi2>0')

variable('log(ak08_chi3)', "log(#chi) (R=0.3)", -10., 10, extra_cut = 'ak08_chi3>0')
variable('log(ca15_chi3)', "log(#chi) (R=0.3)", -10., 10, extra_cut = 'ca15_chi3>0')

variable('npv', "Number of primary vertices", -0.5, 39.5)
variable('pt', "Parton p_{T}", 0, 39.51800)
variable('eta', "Parton #eta", -2.5, 2.5)




