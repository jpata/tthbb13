#!/usr/bin/env python

## To run this script, you need to install pandas (http://pandas.pydata.org/)
import pandas, sys
import matplotlib.pyplot as plt
import numpy as np

def get_event_set(d):
    """
    Returns the set of events in a DataFrame.

    d - pandas DataFrame
    returns: set of (run, lumi, event) triplets.
    """
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

def get_events(d, evlist):
    s = []
    for run, lumi, event in evlist:
        evstr = "(run=={0}) & (lumi=={1}) & (event=={2})".format(run, lumi, event)
        s1 = d.eval(evstr)
        s += [s1]
    tot = np.zeros(len(d), dtype=np.bool)
    if len(s) > 0:
        tot = s[0]
        for x in s[1:]:
            tot = tot | x
    return tot

def compare_events(d1, d2, evids, varlist, fi):
    for (run, lumi, event) in evids:
        evstr = "(run=={0}) & (lumi=={1}) & (event=={2})".format(run, lumi, event)
        s1 = d1.eval(evstr)
        s2 = d2.eval(evstr)
        in_d1 = sum(s1) == 1
        in_d2 = sum(s2) == 1
        fi.write("{0}:{1}:{2}\n".format(run, lumi, event))
        fi.write("in D1={0} D2={1}\n".format(in_d1, in_d2))
        if in_d1 and in_d2:
            #print "common ({0}, {1}, {2}),".format(run, lumi, event)
            for v in varlist:
                fi.write("C* {0} {1} {2}\n".format(v, d1[s1][v].as_matrix()[0], d2[s2][v].as_matrix()[0]))
        elif in_d1:
            #print "d1 ({0}, {1}, {2}),".format(run, lumi, event)
            for v in varlist:
                fi.write("D1* {0} {1}\n".format(v, d1[s1][v].as_matrix()[0]))
        elif in_d2:
            #print "d2 ({0}, {1}, {2}),".format(run, lumi, event)
            for v in varlist:
                fi.write("D2* {0} {1}\n".format(v, d2[s2][v].as_matrix()[0]))

vars = [
    "n_jets", "n_btags",
    "is_SL", "is_DL",
    "lep1_pt",
    "lep1_iso",
    "lep1_pdgId",
    "lep2_pt",
    "lep2_iso",
    "lep2_pdgId",
    "jet1_pt", "jet2_pt", "jet3_pt", "jet4_pt",
    "jet1_CSVv2", "jet2_CSVv2", "jet3_CSVv2", "jet4_CSVv2",
    "MET_pt", "MET_phi",
    "met_passed",
    "bWeight",
    "ttHFCategory",
    "mll",
    "mll_passed",
]

cuts = [
#    "(is_SL==1) | (is_DL==1)",
#    "(is_SL==1)",
#    "(is_DL==1)",
    "(is_SL==1) & (n_jets==4) & (n_btags==3) & (mll_passed==1) & (met_passed==1)",
    "(is_SL==1) & (n_jets==4) & (n_btags==4) & (mll_passed==1) & (met_passed==1)",
    "(is_SL==1) & (n_jets==5) & (n_btags==3) & (mll_passed==1) & (met_passed==1)",
    "(is_SL==1) & (n_jets==5) & (n_btags>=4) & (mll_passed==1) & (met_passed==1)",
    "(is_SL==1) & (n_jets>=6) & (n_btags==2) & (mll_passed==1) & (met_passed==1)",
    "(is_SL==1) & (n_jets>=6) & (n_btags==3) & (mll_passed==1) & (met_passed==1)",
    "(is_SL==1) & (n_jets>=6) & (n_btags>=4) & (mll_passed==1) & (met_passed==1)",
    "(is_DL==1) & (n_jets==3) & (n_btags==2) & (mll_passed==1) & (met_passed==1)",
    "(is_DL==1) & (n_jets>=3) & (n_btags==3) & (mll_passed==1) & (met_passed==1)",
    "(is_DL==1) & (n_jets>=4) & (n_btags==2) & (mll_passed==1) & (met_passed==1)",
    "(is_DL==1) & (n_jets>=4) & (n_btags>=4) & (mll_passed==1) & (met_passed==1)",
]

cuts_names = [
#    "inclusive",
#    "SL",
#    "DL",
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

def compareTwo(d1, d2, d1Name, d2Name, sample):
    print_detail = False
    commons = [compare(d1, d2, cut) for cut in cuts]
    prefix = d1Name + "_" + d2Name + "_" + sample
    
    plt.figure(figsize=(6,5))
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
    plt.legend(loc=(1.1,1.0), frameon=False)
    a2 = plt.axes((0.0,0.0, 1.0,0.45))
    plt.plot(xs+0.2, map(lambda x: float(len(x[1]))/float(len(x[0])) if len(x[0])>0 else 0, commons), color="black", lw=0, marker="o")
    plt.plot(xs+0.6, map(lambda x: float(len(x[2]))/float(len(x[0])) if len(x[0])>0 else 0, commons), color="red", lw=0, marker="o")
    #plt.ylim(0.0,0.1)
    plt.xticks(xs+0.4, cuts_names, rotation=90);
    plt.axhline(0.0, color="blue")
    plt.grid()
    plt.xlabel("category", fontsize=16)
    plt.ylabel("difference / common", fontsize=16)
    plt.savefig(prefix+".png", dpi=800, bbox_inches='tight')

    outfile = open(prefix + "_results.html", "w")
    outfile.write("<h1>A={0} B={1} sample={2}</h1>".format(d1Name, d2Name, sample))
    outfile.write("<br><img src=\"{0}.png\" style=\"width:600px;height:500px;\"> <br>".format(prefix))
    for icat in range(len(commons)):

        newvars_A = [(v, pairA + "_" + v) for v in vars]
        newvars_B = [(v, pairB + "_" + v) for v in vars]
        d1_renamed = d1.rename(columns=dict(newvars_A))
        d1_renamed = d1_renamed[["run", "lumi", "event"]+[v[1] for v in newvars_A]]
        d2_renamed = d2.rename(columns=dict(newvars_B))
        d2_renamed = d2_renamed[["run", "lumi", "event"]+[v[1] for v in newvars_B]]

        c = list(commons[icat][0])
        inB = list(commons[icat][1])
        inA = list(commons[icat][2])
        sel_d1 = list(commons[icat][3])
        sel_d2 = list(commons[icat][4])
        outfile.write("<hr>\n")
        #outfile.write("******************************************************************<br>")
        outfile.write("<h2>{6}. {7}</h2> cut='{0}' A={1} B={2} common={3} inAonly={4} inBonly={5}".format(
            cuts[icat], len(sel_d1), len(sel_d2), len(c), len(inA), len(inB), icat, cuts_names[icat]
        ))
        if len(c) == 0:
            outfile.write("<br>Nothing common in {0}<br>".format(cuts[icat]))
            continue
        #outfile.write("******************************************************************<br>")

        conc = pandas.merge(d1_renamed, d2_renamed, on=["run", "lumi", "event"], how='outer')
        totvars = ["run", "lumi", "event"]
        for ivar in range(len(vars)):
            totvars += [newvars_A[ivar][1], newvars_B[ivar][1]]
        conc = conc[totvars]
        if len(c)>0:
            ec1 = get_events(conc, c[:20])
            outfile.write("<h3>Printing first 20 events that are common</h3>")
            outfile.write(str(conc[ec1].to_html()) + "<br>")
            #outfile.write("-------------------------------------------<br>")


        if len(inA)>0:
            ec1 = get_events(conc, inA[:10])
            outfile.write("<h3>Printing first 10 events that are only in A</h3>")
            outfile.write(str(conc[ec1].to_html()) + "<br>")
            #outfile.write("-------------------------------------------<br>")

        if len(inB)>0:
            ec1 = get_events(conc, inB[:10])
            outfile.write("<h3>Printing first 10 events that are only in B</h3>")
            outfile.write(str(conc[ec1].to_html()) + "<br>")
            #outfile.write("-------------------------------------------<br>")

        # if print_detail:
        #     outfile.write("Printing first 3 events that are common\n")
        #     ec = get_events(d1, c[:3])
        #     for v in vars:
        #         outfile.write(d1.loc[get_events(d1, c[:3]), v] + "\n")
        #         d2.loc[get_events(d2, c[:3]), c]
        #     outfile.write("{0}\n".format(d1.loc[get_events(d1, c[:3]), vars]))
        #     outfile.write("Printing first 3 events that are only in A\n")
        #     #outfile.write("{0}\n".format(d1.loc[get_events(d1, inA[:3]), vars]))
        #     outfile.write("-------------------------------------------\n")
        #     # for ev in inA[:3]:
        #     #     compare_events(d1, d2, [ev], vars)
        #     outfile.write("Printing first 3 events that are only in B\n")
        #     outfile.write("-------------------------------------------\n")
        #     # for ev in inB[:3]:
        #     #     outfile.write("#####\n")
        #     #     compare_events(d1, d2, [ev], vars, outfile)
    outfile.close()

data = {}
for x in ["eth", "desy", "kit", "ihep", "osu"]:
    data[x] = {}

data["eth"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/eth/v13/tth.csv")
data["eth"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/eth/v13/ttjets.csv")

data["desy"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/desy/v5/tth.csv")
data["desy"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/desy/v5/ttjets.csv")
# 
# data["kit"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/kit/tth.csv")
# data["kit"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/kit/ttjets.csv")

data["ihep"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/ihep/v3/tth.csv")
data["ihep"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/ihep/v3/ttjets.csv")
# 
# data["osu"]["sig"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/osu/tth.csv")
# data["osu"]["bkg"] = pandas.read_csv("/Users/joosep/Dropbox/tth/sync/endof2015/osu/ttjets.csv")

for sample in ["sig", "bkg"]:
    for pairA, pairB in [
    ("eth", "desy"),
    #("eth", "kit"),
    #("eth", "osu"),
    ("eth", "ihep"),
    # ("desy", "kit"),
    ("desy", "ihep"),
    # ("kit", "ihep"),
    # ("osu", "kit"),
    # ("osu", "desy"),
    # ("osu", "ihep"),
    ]:
        d1 = data[pairA][sample]
        d2 = data[pairB][sample]
        compareTwo(d1, d2, pairA, pairB, sample)
