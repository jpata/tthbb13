import ROOT, sys, re

def scan(tf, pref=""):
    for k in tf.GetListOfKeys():
        obj = k.ReadObj()
        cn = k.GetClassName()
        if cn == "TTree":
            print pref + "/" + obj.GetName(),"=", obj.GetEntries()
        if cn == "TDirectoryFile":
            scan(obj, pref+"/"+obj.GetName())

for fn in sys.argv[1:]:
    fn = fn.split()[0]
    if fn.endswith(".root"):
        tf = ROOT.TFile.Open(fn)
        scan(tf, fn+":")
    else:
        print "skipping", fn
