import TTH.Plotting.Datacards.Samples as Samples
import ROOT, json

#entries per job
perjob = 50000

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

#nbins_mem = 6
#nbins_bdt = 6
nbins_mem = 36
nbins_bdt = 40

ijob = 0
for samp in Samples.samples_dict.keys():
    s = Samples.samples_dict[samp]
    tf = ROOT.TChain("tree")
    filenames = getattr(s, "filenames", [s])
    for f in s.filenames:
        tf.AddFile(f)
    nEntries = tf.GetEntries()
    for ch in chunks(range(nEntries), perjob):
        #default configuration
        ijob += 1
