import ROOT, sys
from collections import Counter

f = ROOT.TFile(sys.argv[1])

t = f.Get("tthNtupleAnalyzer/events")

if not t or t.IsZombie():
    raise Exception("could not open ttree tthNtupleAnalyzer/events")

if t.GetEntries() != 100:
    raise Exception("number of entries != 100: %s" % t.GetEntries())

brs = t.GetListOfBranches()

print "Branch list: "
print "B", "branch", "L", "list of leaves"
for br in brs:
    print "B", br.GetName(), "L", [(l.GetName(), l.GetTypeName()) for l in br.GetListOfLeaves()]

njets = []
nleps = []
lep_ids = []
lep_isos = []
for ev in t:
    njets += [ev.n__jet]
    nleps += [ev.n__lep]

    for nl in range(0, ev.n__lep):
        lep_id = ev.lep__id[nl]
        lep_ids += [lep_id]
        lep_isos += [ev.lep__rel_iso[nl]]

if njets != [23, 33, 28, 24, 18, 20, 12, 25, 16, 16, 22, 18, 29, 22, 31, 22, 15, 33, 30, 20, 19, 28, 32, 23, 29, 21, 13, 29, 20, 15, 20, 17, 17, 13, 19, 18, 17, 20, 18, 22, 17, 14, 21, 17, 22, 21, 14, 20, 22, 20, 19, 23, 24, 22, 21, 26, 15, 21, 29, 24, 19, 11, 18, 28, 17, 14, 16, 26, 17, 26, 27, 15, 29, 7, 23, 25, 15, 22, 17, 23, 31, 16, 21, 16, 23, 24, 23, 18, 20, 19, 28, 23, 28, 18, 16, 26, 10, 20, 16, 20]:
    raise Exception("number of jets seems incorrect: %s" % njets)
if nleps != [6, 3, 6, 4, 4, 14, 8, 5, 3, 6, 9, 4, 2, 19, 4, 4, 8, 2, 11, 9, 9, 6, 5, 6, 7, 6, 3, 3, 7, 3, 5, 1, 3, 8, 3, 9, 5, 6, 7, 10, 2, 4, 6, 6, 6, 3, 4, 7, 4, 7, 11, 6, 5, 10, 11, 10, 5, 8, 6, 7, 9, 8, 8, 2, 5, 4, 3, 14, 9, 2, 8, 7, 7, 2, 5, 7, 4, 6, 8, 13, 6, 6, 4, 6, 4, 8, 3, 5, 4, 2, 7, 4, 8, 4, 8, 2, 4, 10, 4, 3]:
    raise Exception("number of leptons seems incorrect: %s" % nleps)

clep_ids = Counter(lep_ids)
if clep_ids != Counter({-13: 124, 13: 115, 15: 99, -15: 97, 11: 95, -11: 74}):
    raise Exception("Incorrect lepton ID counts: %s" % clep_ids)

print lep_isos

print "all tests passed!"
