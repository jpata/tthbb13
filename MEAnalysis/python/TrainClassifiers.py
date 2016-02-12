"""

"""

########################################
# Imports
########################################

import pickle

import matplotlib as mpl
mpl.use('Agg')
import sklearn
import numpy as np
import matplotlib.pyplot as plt
import pandas, root_numpy
from sklearn.ensemble import GradientBoostingClassifier

from TTH.Plotting.joosep.plotlib import *


########################################
# Configuration
########################################

brs = [
    "is_signal",
    "j1j2_mass", "j1j3_mass", "j2j3_mass", "j1j2j3_mass", "frec", 
    "min_btagCSV", "max_btagCSV",
    "mean_btagCSV", "variance_btagCSV",
 ]

ds = []
path = "/shome/gregor/tth/gc/GCf4625db4aa6a/cfg_noME/ttHTobb_M125_13TeV_powheg_pythia8/"

for fn in [path + "outputhadtop_3j.root"]:
    d = root_numpy.root2rec(fn, branches=brs)
    d = pandas.DataFrame(d)    
    ds += [d]

df = pandas.concat(ds)

print df.shape
print df.groupby('is_signal')["is_signal"].count()

#df["j1j2j3_massnew"] = df["j1j2j3_mass"]
#df.loc[df["j1j2j3_massnew"] > 400,"j1j2j3_massnew"] = 400
#brs.append("j1j2j3_massnew")

#df["frecnew"] = df["frec"]
#df.loc[df["frecnew"] > 0.4,"frecnew"] = 0.4
#brs.append("frecnew")


########################################
# Helper: train
########################################

def train(df, var,  **kwargs):
    
    df_shuf = df.iloc[np.random.permutation(np.arange(len(df)))]
    
    cls = GradientBoostingClassifier(
        n_estimators=kwargs.get("ntrees", 200),
        learning_rate=kwargs.get("learning_rate", 0.1),
        max_depth=kwargs.get("depth", 2),
        min_samples_split=kwargs.get("min1", 1),
        min_samples_leaf=kwargs.get("min2", 1),
        subsample=kwargs.get("subsample", 1.0),
        verbose=kwargs.get("verbose", False)
    )


    cls = cls.fit(df_shuf[var], df_shuf["is_signal"])
    cls.varlist = var

    return cls


########################################
# Helper: rocplot
########################################

def rocplot(cut, title, classifiers, labels):
    plt.plot([0,1],[0,1], color="black", lw=2)
    #sel = dtest.eval(cut) 
    #subdf = dtest[sel]
    sig = dtest["is_signal"]==1
    bkg = dtest["is_signal"]!=1
    
    rocs = []
    idx = 0
    for cls in classifiers:
        probs1 = cls.predict_proba(dtest[sig][cls.varlist])[:, 1]
        probs2 = cls.predict_proba(dtest[bkg][cls.varlist])[:, 1]

        h1 = make_df_hist((101,0,1), probs1)
        h2 = make_df_hist((101,0,1), probs2)
        r, e = calc_roc(h1, h2)
        rocs += [(r,e)]
        plt.plot(r[:, 0], r[:, 1], label=labels[idx], lw=1, ls="--")
        #plt.fill_between(r[:,0], r[:,1]+e[:,1], r[:,1]-e[:,1],alpha=0.1, color="black")
        #plt.fill_betweenx(r[:,1], r[:,0]-e[:,0], r[:,0]+e[:,0],alpha=0.1, color="black")
        idx += 1

    plt.xlabel("true match efficiency", fontsize=16)
    plt.ylabel("fake match efficiency", fontsize=16)
    #plt.yscale('log')


    #var = "lr0"
    #if "dl" in title:
    #    var = "lr1"
    
    #h1 = make_df_hist((101,0,1), dtest[sig][var]) #dtest[sig]["genWeight"])
    #h2 = make_df_hist((101,0,1), dtest[bkg][var]) #dtest[bkg]["genWeight"])
    #r, e = calc_roc(h1, h2)
    #plt.plot(r[:, 0], r[:, 1], label="MEM 022", color="black", lw=1)
    #plt.fill_between(r[:,0], r[:,1]+e[:,1], r[:,1]-e[:,1],alpha=0.1, color="black")

    #plt.title(title + "\n$N_s=%d\\ N_b=%d$"%(np.sum(["id"]==0), np.sum(subdf["id"]==1)))
    plt.legend(loc=2)
    plt.xlim(0,1);plt.ylim(0,1);


df_shuf = df.iloc[np.random.permutation(len(df))]

nsig = df_shuf["is_signal"]==1
nbkg = df_shuf["is_signal"]==0

d_bkg_tr = df_shuf[nbkg][:sum(nsig)/2]
d_sig_tr = df_shuf[nsig][:sum(nsig)/2]

d_bkg_te = df_shuf[nbkg][sum(nbkg)/2:]
d_sig_te = df_shuf[nsig][sum(nsig)/2:]

dtrain = pandas.concat([d_bkg_tr, d_sig_tr])
dtest = pandas.concat([d_bkg_te, d_sig_te])


for br in brs:

    xmin = min(df[br])
    xmax = max(df[br])

    plt.clf()
    plt.hist(df.loc[df["is_signal"]==0,br].as_matrix(),color="red", bins=np.linspace(xmin,xmax,50),normed=True, alpha=0.4)
    plt.hist(df.loc[df["is_signal"]==1,br].as_matrix(),color="blue",bins=np.linspace(xmin,xmax,50),normed=True, alpha=0.4)
    
    plt.savefig("nom_{0}.png".format(br))

cls = train(
    dtrain,
    ["j1j2j3_mass", "frec", "min_btagCSV", "max_btagCSV"],
    ntrees=50,
    learning_rate=0.1,
    max_depth=4,
    subsample=.8,
    verbose=True
)

cls_meanvarCSV = train(
    dtrain,
    ["j1j2j3_mass", "frec", "mean_btagCSV", "variance_btagCSV"],
    ntrees=50,
    learning_rate=0.1,
    max_depth=4,
    subsample=.8,
    verbose=True
)

plt.clf()


plt.hist(cls.predict_proba(dtest.loc[
    dtest.eval("(is_signal==0)"), cls.varlist
    ])[:,1], bins=np.linspace(0,1,51), color="red", normed=True, alpha=0.4
);
plt.hist(cls.predict_proba(dtest.loc[
    dtest.eval("(is_signal==1)"), cls.varlist
    ])[:,1], bins=np.linspace(0,1,51), color="blue", alpha=0.4, normed=True
);


cls.predict_proba(dtest.loc[dtest.eval("(is_signal==1)"), cls.varlist])[:,0]
plt.savefig("foo.png")



plt.clf()
rocplot("", "foo",[cls, cls_meanvarCSV],["kin+min/max","kin+mean/var"])
plt.savefig("ROC.png")


f = open("cls_top_resolved.pickle","wb")
pickle.dump(cls_meanvarCSV, f)
f.close()





