import ROOT, sys, re, os

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
        if tf!=None and not tf.IsZombie():
            print fn, int(tf.GetSize())
            scan(tf, fn+":")
        else:
            print "error", fn
    else:
        print "skipping", fn
