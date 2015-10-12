import TTH.Plotting.Datacards.MiniSamples as Samples
import ROOT, json

#entries per job
perjob = 500000

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

ijob = 0
for samp in Samples.samples_dict.keys():
    s = Samples.samples_dict[samp]
    tf = ROOT.TChain("tree")
    tf.AddFile(s)
    nEntries = tf.GetEntries()
    for ch in chunks(range(nEntries), perjob):
        #default configuration
        ret = {
            "filenames": [s],
            "lumi": 10000.0,
            "process": samp,
            "outputFile": "ControlPlotsSparse_{0}.root".format(ijob),
            "firstEntry": ch[0],
            "numEntries": len(ch),
            "printEvery": 0,
            "sparseAxes": [
                {
                    "func": "mem_SL_0w2h2t",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 6
                },
                {
                    "func": "numJets",
                    "xMin": 4,
                    "xMax": 7,
                    "nBins": 3
                },
                {
                    "func": "nBCSVM",
                    "xMin": 2,
                    "xMax": 5,
                    "nBins": 3
                },
                {
                    "func": "nBoosted",
                    "xMin": 0,
                    "xMax": 2,
                    "nBins": 2
                },
                {
                    "func": "btag_LR_4b_2b_logit",
                    "xMin": -20,
                    "xMax": 20,
                    "nBins": 10
                },
                {
                    "func": "topCandidate_mass",
                    "xMin": 100,
                    "xMax": 200,
                    "nBins": 6
                },
                {
                    "func": "Wmass",
                    "xMin": 40,
                    "xMax": 120,
                    "nBins": 6
                }
            ]
        }
        of = open("job_{0}.json".format(ijob), "w")
        of.write(json.dumps(ret, indent=2))
        of.close()
        ijob += 1
