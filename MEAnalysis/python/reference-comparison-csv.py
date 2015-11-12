import pandas, sys
import matplotlib.pyplot as plt
import numpy as np

file0 = sys.argv[1]
file1 = sys.argv[2]

d1 = pandas.read_csv(file0)
d2 = pandas.read_csv(file1)

print "D1", d1.shape
print "D2", d2.shape
print_detail = True

def get_event_set(d):
    s1 = set([])
    for r in d[["run", "lumi", "event"]].iterrows():
        s1.add((int(r[1][0]), int(r[1][1]), int(r[1][2])))
    return s1

def compare(d1, d2, sel):
    s1 = d1.eval(sel)
    s2 = d2.eval(sel)
    evs1 = get_event_set(d1[s1])
    evs2 = get_event_set(d2[s2])
    
    common = evs1.intersection(evs2)

    missing_s2 = evs1.difference(evs2)
    missing_s1 = evs2.difference(evs1)
    #print sel, len(evs1), len(evs2), len(common), len(missing_s1), len(missing_s2)

    #print "a) common", len(common)
    #print "b) in {0}, not in {1}".format(nd1, nd2), len(missing_s1)
    #print "c) not in {0}, in {1}".format(nd1, nd2), len(missing_s2)
    return common, missing_s1, missing_s2, evs1, evs2

def compare_events(d1, d2, evids, varlist):
    for (run, lumi, event) in evids:
        evstr = "(run=={0}) & (lumi=={1}) & (event=={2})".format(run, lumi, event)
        s1 = d1.eval(evstr)
        s2 = d2.eval(evstr)
        in_d1 = sum(s1) == 1
        in_d2 = sum(s2) == 1
        print "{0}:{1}:{2}".format(run, lumi, event)
        print "in D1={0} D2={1}".format(in_d1, in_d2)
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

vars = [
    "n_jets", "n_btags",
    "is_SL", "is_DL",
    "lep1_pt", "lep1_iso",
    "jet1_pt", "jet2_pt", "jet3_pt", "jet4_pt",
    "jet1_CSVv2", "jet2_CSVv2", "jet3_CSVv2", "jet4_CSVv2",
    "MET_pt", "MET_phi"
]

cuts = [
    "(is_SL==1) | (is_DL==1)",
    "(is_SL==1)",
    "(is_DL==1)",
    "(is_SL==1) & (n_jets==4) & (n_btags==3)",
    "(is_SL==1) & (n_jets==4) & (n_btags==4)",
    "(is_SL==1) & (n_jets==5) & (n_btags==3)",
    "(is_SL==1) & (n_jets==5) & (n_btags>=4)",
    "(is_SL==1) & (n_jets>=6) & (n_btags==2)",
    "(is_SL==1) & (n_jets>=6) & (n_btags==3)",
    "(is_SL==1) & (n_jets>=6) & (n_btags>=4)",
    "(is_DL==1) & (n_jets==3) & (n_btags==2)",
    "(is_DL==1) & (n_jets>=3) & (n_btags==3)",
    "(is_DL==1) & (n_jets>=4) & (n_btags==2)",
    "(is_DL==1) & (n_jets>=4) & (n_btags>=4)",
]

cuts_names = [
    "inclusive",
    "SL",
    "DL",
    "SL 4J 3T",
    "SL 4J 4T",
    "SL 5J 3T",
    "SL 5J 4+T",
    "SL 6+J 2T",
    "SL 6+J 3T",
    "SL 6+J 4+T",
    "DL 3J 2T",
    "DL 3+J 3T",
    "DL 4+J 2T",
    "DL 4+J 4+T"
]

commons = [compare(d1, d2, cut) for cut in cuts]

plt.figure(figsize=(4,5))
a1 = plt.axes((0.0,0.5, 1.0,0.5))
xs = np.array(range(len(cuts)))
plt.bar(xs, map(lambda x: len(x[0]), commons), label="common in A and B", color="gray")
plt.errorbar(xs+0.2, map(lambda x: len(x[0]), commons), map(lambda x: len(x[1]), commons), label="in B, not in A", color="black", lw=0, elinewidth=2)
plt.errorbar(xs+0.6, map(lambda x: len(x[0]), commons), map(lambda x: len(x[2]), commons), label="in A, not in B", color="red", lw=0, elinewidth=2)
plt.xticks(xs, []);
#plt.grid()
#plt.ylim(bottom=1)
#plt.yscale("log")
plt.ylabel("number of MC events", fontsize=16)
plt.title("A={0} B={1}".format("file1", "file2"), fontsize=20)
plt.legend(loc="best", frameon=False)
a2 = plt.axes((0.0,0.0, 1.0,0.45))
plt.plot(xs+0.2, map(lambda x: float(len(x[1]))/float(len(x[0])) if len(x[0])>0 else 0, commons), color="black", lw=0, marker="o")
plt.plot(xs+0.6, map(lambda x: float(len(x[2]))/float(len(x[0])) if len(x[0])>0 else 0, commons), color="red", lw=0, marker="o")
#plt.ylim(0.0,0.1)
plt.xticks(xs+0.4, cuts_names, rotation=90);
plt.axhline(0.0, color="blue")
plt.grid()
plt.xlabel("category", fontsize=16)
plt.ylabel("difference / common", fontsize=16)
plt.savefig("sl.pdf")
plt.clf()

for icat in range(len(commons)):
    c = list(commons[icat][0])
    inA = list(commons[icat][1])
    inB = list(commons[icat][2])
    sel_d1 = list(commons[icat][3])
    sel_d2 = list(commons[icat][4])
    if print_detail:
        print "******************************************************************"
    print cuts[icat], "A", len(sel_d1), "B", len(sel_d2), "common", len(c), "Aonly", len(inA), "Bonly", len(inB)
    if print_detail:
        print "******************************************************************"

    if print_detail:
        print "Printing first 3 events that are common"

        print "Printing first 3 events that are only in A"
        print "-------------------------------------------"
        for ev in inA[:3]:
            compare_events(d1, d2, [ev], vars)
        print "Printing first 3 events that are only in B"
        print "-------------------------------------------"
        for ev in inB[:3]:
            print "#####"
            compare_events(d1, d2, [ev], vars)
# list(commons_sl[0][1])[:2]
# 
# 
# # In[68]:
# 
# list(commons_sl[0][2])[:2]
# 
# 
# # In[69]:
# 
# compare_events(d1, d2, list(commons_dl[0][0]), vars)
# 
# 
# # ### Not in D1
# 
# # In[ ]:
# 
# # In[258]:
# 
# compare_events(d1, d2, list(commons_dl[1][1])[:5], vars)
# 
# 
# # ### Not in D2
# 
# # In[300]:
# 
# compare_events(d1, d2, list(commons_dl[0][2]), vars)
# 
# 
# # In[90]:
# 
# d1[d1["event"] == 275234][["is_SL", "is_DL", "event", "lep1_pdgId", "lep2_pdgId", "lep1_pt", "lep2_pt"]].head()
