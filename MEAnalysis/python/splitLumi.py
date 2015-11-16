from FWCore.PythonUtilities.LumiList import LumiList
import sys

ll = LumiList(filename=sys.argv[1])
lumis = ll.getLumis()
nblock = 0

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

for lumiblock in chunks(lumis, 5):
    print lumiblock
    nblock += 1
    ll2 = LumiList(lumis=lumiblock)
    of = open(sys.argv[2] + "/block_{0}.json".format(nblock), "w")
    of.write(str(ll2))
    of.close()
