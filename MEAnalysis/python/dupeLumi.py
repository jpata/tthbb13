import ROOT, numpy, sys

run = numpy.zeros(1, dtype=numpy.uint64)
lumi = numpy.zeros(1, dtype=numpy.uint64)
event = numpy.zeros(1, dtype=numpy.uint64)

infiles = sys.argv[1:]

lumidict = {}

for infile in infiles:
    tf = ROOT.TFile(infile)
    tt = tf.Get("tree")
    
    tt.SetBranchAddress("run", run)
    tt.SetBranchAddress("lumi", lumi)
    tt.SetBranchAddress("evt", event)
    
    tt.SetBranchStatus("*", False)
    for br in ["run", "lumi", "evt"]:
        tt.SetBranchStatus(br, True)
    
    for i in range(tt.GetEntries()):
        tt.GetEntry(i)
        if not lumidict.has_key((run[0], lumi[0], event[0])):
            lumidict[(run[0], lumi[0], event[0])] = [(infile, i)]
        else:
            lumidict[(run[0], lumi[0], event[0])] += [(infile, i)]
    print "scanned", infile, i
    tf.Close()
for (k, v) in lumidict.items():
    if len(v) > 1:
        print k, len(v)
