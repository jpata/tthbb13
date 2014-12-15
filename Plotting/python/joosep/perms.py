import ROOT, sys, numpy

tf = ROOT.TFile(sys.argv[1])

tt = tf.Get("tree")

ps = numpy.zeros(60, dtype=numpy.int32)
n = numpy.zeros(1, dtype=numpy.int32)
tt.SetBranchAddress("perm_to_gen_s", ps)
tt.SetBranchAddress("nPermut_s", n)

n1 = 0
n2 = 0

for i in range(tt.GetEntries()):

    tt.GetEntry(i)

    s = ""

    for j in range(n[0]):
        p = int(ps[j])
        if p == 111111:
            n1 += 1
            break
        if p == 100111:
            n2 += 1
            break

print int(tt.GetEntries())
print n1, n2
