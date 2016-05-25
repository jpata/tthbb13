#######################################
# Imports
########################################

from TrainClassifiersBase import *


########################################
# Configuration
########################################

brs = ["evt", 
       "pt", "eta", "top_size", 
       "ak08_pt",
       "ak08_tau3", "ak08_tau2",
       "ak08softdropz10b00forbtag_btag", 
       "ak08softdropz10b00_mass",
       "ak08softdropz10b00_masscal",

       "ak08puppi_tau3", "ak08puppi_tau2",
       "ak08puppisoftdropz10b00forbtag_btag", 
       "ak08puppisoftdropz10b00_mass",
       "ak08puppisoftdropz10b00_masscal",
]

to_plot = [["pt", 750, 1050, "Parton pT [GeV]"],
           ["eta", -3, 3, "Parton eta"],
           ["top_size", 0, 3, "Top Size"],
           ["ak08_tau3_over_tau2",0, 1., "AK08 tau3/tau2"],
           ["ak08softdropz10b00forbtag_btag", 0, 1., "AK08 b-tag discriminator"],
           ["ak08softdropz10b00_mass", 0, 300, "AK08 softdrop mass [GeV]"],
           ["ak08softdropz10b00_masscal", 0, 300, "AK08 softdrop mass [GeV]"],

           ["ak08puppi_tau3_over_tau2",0, 1., "AK08 Puppi tau3/tau2"],
           ["ak08puppisoftdropz10b00forbtag_btag", 0, 1., "AK08 Puppi b-tag discriminator"],
           ["ak08puppisoftdropz10b00_mass", 0, 300, "AK08 Puppi softdrop mass [GeV]"],
           ["ak08puppisoftdropz10b00_masscal", 0, 300, "AK08 Puppi calibrated softdrop mass [GeV]"],
           ]

colors = ['black', 'red','blue','green','orange','green','magenta']

class_names = {0: "background",
               1: "signal"}

classes = sorted(class_names.keys())

infname_sig = "/scratch/gregor/ntop_x6_zprime_m2000-tagging-weighted.root"
infname_bkg = "/scratch/gregor/ntop_x6_qcd_800_1000-tagging-weighted.root"

min_pt = 801
max_pt = 999
max_eta = 1.5
min_reco_pt = 500

fiducial_cut = "(pt>{0}) && (pt<{1}) && (fabs(eta) < {2}) && (ak08_pt > {3})".format(min_pt, 
                                                                                     max_pt, 
                                                                                     max_eta,
                                                                                     min_reco_pt)


########################################
# Prepare data
########################################

# Get signal events
d_sig = root_numpy.root2rec(infname_sig, branches=brs, selection = fiducial_cut)
df_sig = pandas.DataFrame(d_sig)    
df_sig["is_signal_new"] = 1

# Get background events
d_bkg = root_numpy.root2rec(infname_bkg, branches=brs, selection = fiducial_cut)
df_bkg = pandas.DataFrame(d_bkg)    
df_bkg["is_signal_new"] = 0

print "Reading Data: Done..."

# Combine
df = pandas.concat([df_sig, df_bkg], ignore_index=True)

# Calculate some extra variables
df["ak08_tau3_over_tau2"] = df["ak08_tau3"]/df["ak08_tau2"]
df["ak08puppi_tau3_over_tau2"] = df["ak08puppi_tau3"]/df["ak08puppi_tau2"]

                                                                                    
########################################
# Plot 
########################################



# 1D Variables
for plotvar in to_plot:

    br = plotvar[0]
    xmin = plotvar[1]
    xmax = plotvar[2]
    name = plotvar[3]

    plt.clf()

    for cls in classes:
        plt.hist(df.loc[df["is_signal_new"]==cls,br].as_matrix(),
                 color=colors[cls+1], 
                 bins=np.linspace(xmin,xmax,50),
                 normed=True, 
                 alpha=0.4,
                 label = class_names[cls]
        )    

    plt.xlabel(name, fontsize=16)
    plt.ylabel("Fraction of Jets", fontsize=16)
    plt.legend(loc=0)

    plt.savefig("input_{0}.png".format(br))


for cls in classes:

    for plotrange in ["full", "zoom"]:

        plt.clf()
        for i_br, br in enumerate(["ak08softdropz10b00_mass",
                                   "ak08softdropz10b00_masscal", 
                                   "ak08puppisoftdropz10b00_mass",
                                   "ak08puppisoftdropz10b00_masscal"]):
                                 
            if plotrange == "full":
                xmin = 0
                xmax = 300
                leg_loc = 1
            elif plotrange == "zoom":
                xmin = 90
                xmax = 210
                leg_loc = 2
                
            name = br

            names = {"ak08softdropz10b00_mass"         : "CHS, Uncal.",
                     "ak08softdropz10b00_masscal"      : "CHS, Cal.",
                     "ak08puppisoftdropz10b00_mass"    : "Puppi, Uncal.",
                     "ak08puppisoftdropz10b00_masscal" : "Puppi, Cal.",
                     }

            plt.hist(df.loc[df["is_signal_new"]==cls,br].as_matrix(),
                     color=colors[i_br], 
                     edgecolor = colors[i_br], 
                     bins=np.linspace(xmin,xmax,50),
                     normed=True, 
                     histtype="step",
                     label = names[br]
                )    

        plt.xlabel("Mass [GeV]", fontsize=16)
        plt.ylabel("Fraction of Jets", fontsize=16)
        plt.legend(loc=leg_loc)

        plt.savefig("input_mass_{0}_{1}.png".format(class_names[cls], plotrange))





plt.clf()


i = 0

for br, cut, name in [

        ["ak08softdropz10b00_masscal", lambda : (df["is_signal_new"]==1) & (df["ak08_tau3_over_tau2"] > 0.51), "CHS, Cal., n-sub cut"],
        ["ak08puppisoftdropz10b00_masscal", lambda : (df["is_signal_new"]==1) & (df["ak08puppi_tau3_over_tau2"] > 0.48), "Puppi, Cal., n-sub cut"]]:
    
    xmin = 90
    xmax = 210

    plt.hist(df.loc[cut(),br].as_matrix(),
             color=colors[i], 
             edgecolor = colors[i], 
             bins=np.linspace(xmin,xmax,50),
             normed=True, 
             histtype="step",
             label = name
        )    

    i+=1

plt.xlabel("Mass [GeV]", fontsize=16)
plt.ylabel("Fraction of Jets", fontsize=16)
plt.legend(loc=2)

plt.savefig("masses.png")






