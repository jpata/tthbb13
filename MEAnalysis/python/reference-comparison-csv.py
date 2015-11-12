
# coding: utf-8

# In[1]:

import pandas


# In[2]:

data = {}
for x in ["osu", "eth", "ethv2", "desy", "desyv2", "ihep", "kit"]:
    data[x] = {}


# In[21]:

#data["osu"]["sig"] =pandas.read_csv("/Users/joosep/Documents/tth/sync/")
data["eth"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/ETH/tth.csv")
data["eth"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/ETH/ttjets.csv")

data["ethv2"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/ETH/cmg//tth.csv")
data["ethv2"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/ETH/cmg/ttjets.csv")

data["ihep"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/IHEP/tth.csv")
data["ihep"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/IHEP/ttjets.csv")

data["desy"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/DESYv2/tth.csv")
data["desy"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/DESYv2/tth.csv")

data["kit"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/KIT/tth.csv")
data["kit"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/KIT/ttjets.csv")


data["osu"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/OSU/tth.csv")
data["osu"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/ref2/OSU/ttjets.csv")


# In[22]:

def get_event_set(d):
    s1 = set([])
    for r in d[["run", "lumi", "event"]].iterrows():
        s1.add((int(r[1][0]), int(r[1][1]), int(r[1][2])))
    return s1


# Using these events sets, we can take the intersection of the two sets
# 
# $$\mathrm{common} = s_1 \cap s_2$$
# 
# And the two set differences
# $$d_1 = s_1 \setminus s_2$$
# $$d_2 = s_2 \setminus s_1$$

# In[23]:

def compare(d1, d2, sel):
    s1 = d1.eval(sel)
    s2 = d2.eval(sel)
    evs1 = get_event_set(d1[s1])
    evs2 = get_event_set(d2[s2])
    
    common = evs1.intersection(evs2)

    missing_s2 = evs1.difference(evs2)
    missing_s1 = evs2.difference(evs1)
    print nd1, nd2, sel, len(evs1), len(evs2), len(common), len(missing_s1), len(missing_s2)

    #print "a) common", len(common)
    #print "b) in {0}, not in {1}".format(nd1, nd2), len(missing_s1)
    #print "c) not in {0}, in {1}".format(nd1, nd2), len(missing_s2)
    return common, missing_s1, missing_s2


# In[24]:

def compare_events(d1, d2, evids, varlist):
    for (run, lumi, event) in evids:
        evstr = "(run=={0}) & (lumi=={1}) & (event=={2})".format(run, lumi, event)
        s1 = d1.eval(evstr)
        s2 = d2.eval(evstr)
        in_d1 = sum(s1) == 1
        in_d2 = sum(s2) == 1
        print run, lumi, event
        print in_d1, in_d2
        if in_d1 and in_d2:
            #print "common ({0}, {1}, {2}),".format(run, lumi, event)
            for v in varlist:
                print "*", v, d1[s1][v].as_matrix()[0], d2[s2][v].as_matrix()[0]
        elif in_d1:
            #print "d1 ({0}, {1}, {2}),".format(run, lumi, event)
            for v in varlist:
                print "*", v, d1[s1][v].as_matrix()[0]
        elif in_d2:
            #print "d2 ({0}, {1}, {2}),".format(run, lumi, event)
            for v in varlist:
                print "*", v, d2[s2][v].as_matrix()[0]


# ### Define datasets and comparison variables

# In[38]:

nd1 = "eth"
nd2 = "kit"


# In[39]:

d1 = data[nd1]["sig"]
d2 = data[nd2]["sig"]
vars = ["n_jets", "n_btags", "lep1_pt", "lep1_iso", "jet1_pt", "jet2_pt", "jet3_pt", "jet4_pt", "jet1_CSVv2", "jet2_CSVv2", "jet3_CSVv2", "jet4_CSVv2"]


# ### How many events are common, in D1 only, in D2 only?

# In[40]:

cuts_sl = [
    "(is_SL==1) & (n_jets==4) & (n_btags==3)",
    "(is_SL==1) & (n_jets==4) & (n_btags==4)",
    "(is_SL==1) & (n_jets==5) & (n_btags==3)",
    "(is_SL==1) & (n_jets==5) & (n_btags>=4)",
    "(is_SL==1) & (n_jets>=6) & (n_btags==2)",
    "(is_SL==1) & (n_jets>=6) & (n_btags==3)",
    "(is_SL==1) & (n_jets>=6) & (n_btags>=4)",
]


# In[41]:

cuts_names_sl = [
    "4J 3T",
    "4J 4T",
    "5J 3T",
    "5J 4+T",
    "6+J 2T",
    "6+J 3T",
    "6+J 4+T"
]


# In[42]:

commons_sl = [compare(d1, d2, cut) for cut in cuts_sl]


# In[43]:

commons_sl = [compare(d1, d2, cut) for cut in cuts_sl]


# In[44]:

cuts_dl = [
    "(is_DL==1) & (n_jets==3) & (n_btags==2)",
    "(is_DL==1) & (n_jets>=3) & (n_btags==3)",
    "(is_DL==1) & (n_jets>=4) & (n_btags==2)",
    "(is_DL==1) & (n_jets>=4) & (n_btags>=4)",
]


# In[45]:

cuts_names_dl = [
    "3J 2T",
    "3+J 3T",
    "4+J 2T",
    "4+J 4+T"
]


# In[46]:

commons_dl = [compare(d1, d2, cut) for cut in cuts_dl]


# In[47]:

commons_dl = [compare(d1, d2, cut) for cut in cuts_dl]


# In[48]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import numpy as np


# In[53]:

plt.figure(figsize=(4,5))
a1 = plt.axes((0.0,0.5, 1.0,0.5))
xs = np.array(range(len(cuts_sl)))
plt.bar(xs, map(lambda x: len(x[0]), commons_sl), label="common in A and B", color="gray")
plt.errorbar(xs+0.2, map(lambda x: len(x[0]), commons_sl), map(lambda x: len(x[1]), commons_sl), label="in B, not in A", color="black", lw=0, elinewidth=2)
plt.errorbar(xs+0.6, map(lambda x: len(x[0]), commons_sl), map(lambda x: len(x[2]), commons_sl), label="in A, not in B", color="red", lw=0, elinewidth=2)
plt.xticks(xs, []);
#plt.grid()
#plt.ylim(bottom=1)
#plt.yscale("log")
plt.ylabel("number of MC events", fontsize=16)
plt.title("A={0} B={1}".format(nd1, nd2), fontsize=20)
plt.legend(loc="best", frameon=False)

a2 = plt.axes((0.0,0.0, 1.0,0.45))
plt.plot(xs+0.2, map(lambda x: float(len(x[1]))/float(len(x[0])) if len(x[0])>0 else 0, commons_sl), color="black", lw=0, marker="o")
plt.plot(xs+0.6, map(lambda x: float(len(x[2]))/float(len(x[0])) if len(x[0])>0 else 0, commons_sl), color="red", lw=0, marker="o")
#plt.ylim(0.0,0.1)
plt.xticks(xs+0.4, cuts_names_sl, rotation=90);
plt.axhline(0.0, color="blue")
plt.grid()
plt.xlabel("category", fontsize=16)
plt.ylabel("difference / common", fontsize=16)


# In[55]:

plt.figure(figsize=(4,5))
a1 = plt.axes((0.0,0.5, 1.0,0.5))
xs = np.array(range(len(cuts_dl)))
plt.bar(xs, map(lambda x: len(x[0]), commons_dl), label="common in A and B", color="gray")
plt.errorbar(xs+0.2, map(lambda x: len(x[0]), commons_dl), map(lambda x: len(x[1]), commons_dl), label="in B, not in A", color="black", lw=0, elinewidth=2)
plt.errorbar(xs+0.6, map(lambda x: len(x[0]), commons_dl), map(lambda x: len(x[2]), commons_dl), label="in A, not in B", color="red", lw=0, elinewidth=2)
plt.xticks(xs, []);
#plt.grid()
plt.ylabel("number of MC events", fontsize=16)
plt.title("A={0} B={1}".format(nd1, nd2), fontsize=20)
#plt.legend(loc="best")

a2 = plt.axes((0.0,0.0, 1.0,0.45))
plt.plot(xs+0.2, map(lambda x: float(len(x[1]))/float(len(x[0])) if len(x[0])>0 else 0, commons_dl), color="black", lw=0, marker="o")
plt.plot(xs+0.6, map(lambda x: float(len(x[2]))/float(len(x[0])) if len(x[0])>0 else 0, commons_dl), color="red", lw=0, marker="o")
#plt.ylim(0.0,0.1)
plt.xticks(xs+0.4, cuts_names_dl, rotation=90);
plt.axhline(0.0, color="blue")
plt.grid()
plt.xlabel("(Njets, Ntags)", fontsize=16)
plt.ylabel("difference / common", fontsize=16)


# In[346]:

plt.figure(figsize=(6,6))
a1 = plt.axes((0.0,0.5, 1.0,0.5))
xs = np.array(range(len(cuts)))
plt.bar(xs, map(lambda x: len(x[0]), commons2), label="common in A and B")
plt.errorbar(xs+0.2, map(lambda x: len(x[0]), commons2), map(lambda x: len(x[1]), commons2), label="in B, not in A", color="black", lw=0, elinewidth=2)
plt.errorbar(xs+0.6, map(lambda x: len(x[0]), commons2), map(lambda x: len(x[2]), commons2), label="in A, not in B", color="red", lw=0, elinewidth=2)
plt.xticks(xs, []);
#plt.grid()
#plt.ylim(0,1000)
plt.ylabel("number of MC events", fontsize=16)
plt.title("A={0} B={1}".format(nd1, nd2), fontsize=20)
plt.legend()

a2 = plt.axes((0.0,0.0, 1.0,0.45))
plt.plot(xs+0.2, map(lambda x: float(len(x[1]))/float(len(x[0])) if len(x[0])>0 else 0, commons2), color="black", lw=0, marker="o")
plt.plot(xs+0.6, map(lambda x: float(len(x[2]))/float(len(x[0])) if len(x[0])>0 else 0, commons2), color="red", lw=0, marker="o")
#plt.ylim(0.0,0.1)
plt.xticks(xs+0.4, cuts, rotation=90);
plt.axhline(0.0, color="blue")
plt.grid()
plt.xlabel("(Njets, Ntags)", fontsize=16)
plt.ylabel("difference / common", fontsize=16)


# ### Events common in datasets

# In[ ]:

list(commons_sl[0][1])[:2]


# In[273]:

list(commons_sl[0][2])[:2]


# In[297]:

compare_events(d1, d2, list(commons_dl[0][0]), vars)


# ### Not in D1

# In[ ]:

sel


# In[258]:

compare_events(d1, d2, list(commons_dl[1][1])[:5], vars)


# ### Not in D2

# In[300]:

compare_events(d1, d2, list(commons_dl[0][2]), vars)


# In[461]:

d1[d1["event"] == 862][["run", "lumi", "event", "lep1_pdgId", "lep2_pdgId", "lep1_iso", "lep2_iso"]].head()


# In[444]:

d2[d2.eval("(run==1) & (lumi==1096) & (event==109590)")][["run", "lumi", "event", "lep1_pdgId", "lep2_pdgId", "lep1_iso", "lep2_iso"]]


# In[299]:

d1[d1.eval("(event==2532028)")]


# In[801]:

d2[d2.eval("(is_DL==1)")]["jet4_pt"].hist(bins=np.linspace(0,100,100))


# In[ ]:



