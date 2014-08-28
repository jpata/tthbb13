import ROOT, sys, re

tf = ROOT.TFile(sys.argv[1])
tt = tf.Get("tthNtupleAnalyzer/events")

pat = sys.argv[2]
rex = re.compile(pat)

nmax = int(sys.argv[3])

if len(sys.argv) == 5:
    lenbranch = sys.argv[4]
else:
    lenbranch = None
brnames = [b.GetName() for b in tt.GetListOfBranches()]
matching_branches = sorted(filter(lambda x: rex.match(x)!=None, brnames))
print "matching branches", matching_branches
i = 1

for ev in tt:
    print "***%d***" % i
    for mb in matching_branches:
        if lenbranch and "Buffer" in getattr(ev, mb).__class__.__name__:
            lx = getattr(ev, lenbranch)
            arr = getattr(ev, mb)
            print mb, [round(arr[x],3) for x in range(lx)]
        else:
            print mb, getattr(ev, mb)
    i += 1
    if i>nmax:
        break
