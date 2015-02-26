from collections import OrderedDict
import ROOT
ROOT.gROOT.SetBatch(True)
import sys, os

cat1 = "syst == 0 && (type==0 || (type==3 && flag_type3>0))"
cat2 = "syst == 0 && (type==1 || (type==3 && flag_type3<=0))"
cat3 = "syst == 0 && type==2 && flag_type2<=999"
cat6 = "syst == 0 && type==6"
sl = "syst == 0 && (Vtype == 2 || Vtype == 3)"
dl = "syst == 0 && (Vtype == 5 ||Vtype == 0 || Vtype == 1)"

cut_cat1_H = "syst==0 && ( type==0 || (type==3 && flag_type3>0)) && btag_LR>=0.995"
cut_cat1_L = "syst==0 && ( type==0 || (type==3 && flag_type3>0)) && btag_LR<0.995 && btag_LR>=0.960"
cut_cat2_H = "syst==0 && ( type==1 || (type==3 && flag_type3<=0) ) && btag_LR>=0.9925"
cut_cat2_L = "syst==0 && ( type==1 || (type==3 && flag_type3<=0) ) && btag_LR<0.9925 && btag_LR>=0.960"
cut_cat3_H = "syst==0 && type==2 && flag_type2<=999 && btag_LR>=0.995"
cut_cat3_L = "syst==0 && type==2 && flag_type2<=999 && btag_LR<0.995 && btag_LR>=0.970"
cut_cat6_H = "syst==0 && type==6 && btag_LR>=0.925"
cut_cat6_L = "syst==0 && type==6 && btag_LR<0.925 && btag_LR>=0.850"

cut_cat1_4tag = "syst==0 && ( type==0 || (type==3 && flag_type3>0)) && numBTagM==4"
cut_cat2_4tag = "syst==0 && ( type==1 || (type==3 && flag_type3<=0) ) && numBTagM==4"
cut_cat3_4tag = "syst==0 && type==2 && flag_type2<=999 && numBTagM==4"
cut_cat6_4tag = "syst==0 && type==6 && numBTagM==4"

cut_cat1_3tag = "syst==0 && ( type==0 || (type==3 && flag_type3>0)) && numBTagM==3"
cut_cat2_3tag = "syst==0 && ( type==1 || (type==3 && flag_type3<=0) ) && numBTagM==3"
cut_cat3_3tag = "syst==0 && type==2 && flag_type2<=999 && numBTagM==3"
cut_cat6_3tag = "syst==0 && type==6 && numBTagM==3"

def get_integral(tt, cut):
	assert(tt != None)
	ROOT.gROOT.cd()
	N = tt.Draw("weight >> h", "weight * ({0})".format(cut))
	h = ROOT.gROOT.Get("h")
	E = ROOT.Double(0)
	I = h.IntegralAndError(1, h.GetNbinsX(), E)
	return round(float(I), 4), round(float(E), 4)

tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("tree")

def splitprint(vs):
	s = " | ".join(map(str, vs))
	s = "| {0} |".format(s)
	print s

v1 = get_integral(tt, sl)
v2 = get_integral(tt, dl)
v3 = get_integral(tt, sl)
v4 = get_integral(tt, dl)

splitprint([
	"btag",
	"cat1", "cat1 err",
	"cat2", "cat2 err",
	"cat3", "cat3 err",
	"cat6", "cat6 err",
])

splitprint(("presel", ) + v1 + v2 + v3 + v4)


v1 = get_integral(tt, cat1)
v2 = get_integral(tt, cat2)
v3 = get_integral(tt, cat3)
v4 = get_integral(tt, cat6)
splitprint(("all", ) + v1 + v2 + v3 + v4)


v1 = get_integral(tt, cut_cat1_H)
v2 = get_integral(tt, cut_cat2_H)
v3 = get_integral(tt, cut_cat3_H)
v4 = get_integral(tt, cut_cat6_H)
splitprint(("blrH", ) + v1 + v2 + v3 + v4)

v1 = get_integral(tt, cut_cat1_L)
v2 = get_integral(tt, cut_cat2_L)
v3 = get_integral(tt, cut_cat3_L)
v4 = get_integral(tt, cut_cat6_L)
splitprint(("blrL", ) + v1 + v2 + v3 + v4)

v1 = get_integral(tt, cut_cat1_4tag)
v2 = get_integral(tt, cut_cat2_4tag)
v3 = get_integral(tt, cut_cat3_4tag)
v4 = get_integral(tt, cut_cat6_4tag)
splitprint(("4t", ) + v1 + v2 + v3 + v4)

v1 = get_integral(tt, cut_cat1_3tag)
v2 = get_integral(tt, cut_cat2_3tag)
v3 = get_integral(tt, cut_cat3_3tag)
v4 = get_integral(tt, cut_cat6_3tag)
splitprint(("3t", ) + v1 + v2 + v3 + v4)