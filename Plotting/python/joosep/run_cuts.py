import ROOT, sys

ROOT.gROOT.SetBatch(True)

from cuts import *
tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("tree")

if "old" in sys.argv:
    #lepton channels by Vtype and nLep
    cut_ee = "(Vtype == 1 && nLep==2)"
    cut_emu = "(Vtype == 4 && nLep==2)"
    cut_mumu = "(Vtype == 0 && nLep==2)"
elif "new" in sys.argv:
    #lepton channels by Vtype and nLep
    cut_ee = "(Vtype == 1 && nLep==2)"
    cut_emu = "(Vtype == 5 && nLep==2)"
    cut_mumu = "(Vtype == 0 && nLep==2)"
else:
    raise Exception("specify old or new in argv")

#number of generated events
if "old" in sys.argv:
    print "events", tt.GetEntries(cut_nom), int(tf.Get("hcounter").GetBinContent(2)/tf.Get("hparam").GetBinContent(31)), int(tf.Get("hcounter").GetBinContent(2)), int(tf.Get("hparam").GetBinContent(31))
elif "new" in sys.argv:
    print "events", tt.GetEntries(cut_nom), int(tf.Get("hcounter").GetBinContent(2)), int(tf.Get("hcounter").GetBinContent(2)), int(tf.Get("hparam").GetBinContent(31))
else:
    raise Exception("specify old or new in argv")


brs = [b.GetName() for b in tt.GetListOfBranches()]
cats = [("all", "(1)")]


if "nMatchSimCs" in brs:
    cats += [("bb", cut_bb), ("bj", cut_bj), ("cc", cut_cc), ("jj", cut_jj)]
#split according to jet multiplicities
for (a, b) in cats:
    print "cat1", a, tt.GetEntries(cut_cat1_H + "&&" + b), tt.GetEntries(cut_cat1_L + "&&" + b)
    print "cat2", a, tt.GetEntries(cut_cat2_H + "&&" + b), tt.GetEntries(cut_cat2_L + "&&" + b)
    print "cat3", a, tt.GetEntries(cut_cat3_H + "&&" + b), tt.GetEntries(cut_cat3_L + "&&" + b)
    print "cat6H", a, tt.GetEntries(cut_cat6_H + "&&" + b), tt.GetEntries(cut_cat6_H + "&&" + b + "&&" + cut_ee), tt.GetEntries(cut_cat6_H + "&&" + b + "&&" + cut_emu), tt.GetEntries(cut_cat6_H + "&&" + b + "&&" + cut_mumu)
    print "cat6L", a, tt.GetEntries(cut_cat6_L + "&&" + b), tt.GetEntries(cut_cat6_L + "&&" + b + "&&" + cut_ee), tt.GetEntries(cut_cat6_L + "&&" + b + "&&" + cut_emu), tt.GetEntries(cut_cat6_L + "&&" + b + "&&" + cut_mumu)

tt.Draw("weight>>h", "", "BATCH")
h = tf.Get("h")
print "weight", h.GetMean(), h.GetRMS()
