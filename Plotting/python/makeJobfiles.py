import TTH.Plotting.Datacards.Samples as Samples
import ROOT, json

#entries per job
perjob = 100000

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

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
        ret = {
            "filenames": filenames,
            "lumi": 2500,
            "process": getattr(s, "name", samp),
            "prefix": getattr(s, "prefix", ""),
            "outputFile": "ControlPlotsSparse_{0}.root".format(ijob),
            "firstEntry": ch[0],
            "numEntries": len(ch),
            "printEvery": 0,
            "sparseAxes": [
                {
                    "func": "counting",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 1 
                },
                {
                    "func": "mem_SL_2w2h2t",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 12
                },
                {
                    "func": "mem_SL_2w2h2t_sj",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 12
                },
                {
                    "func": "mem_SL_0w2h2t",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 12
                },
                {
                    "func": "mem_DL_0w2h2t",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 12
                },
                {
                    "func": "tth_mva",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 12
                },
                {
                    "func": "common_bdt",
                    "xMin": -1,
                    "xMax": 1,
                    "nBins": 12
                },
                {
                    "func": "numJets",
                    "xMin": 3,
                    "xMax": 7,
                    "nBins": 4
                },
                {
                    "func": "nBCSVM",
                    "xMin": 1,
                    "xMax": 5,
                    "nBins": 4
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
                    "nBins": 50
                },
                {
                    "func": "topCandidate_mass",
                    "xMin": 100,
                    "xMax": 200,
                    "nBins": 6
                },
                {
                    "func": "topCandidate_fRec",
                    "xMin": 0,
                    "xMax": 0.4,
                    "nBins": 6
                },
                {
                    "func": "topCandidate_n_subjettiness",
                    "xMin": 0,
                    "xMax": 1,
                    "nBins": 6
                },
                {
                    "func": "Wmass",
                    "xMin": 40,
                    "xMax": 120,
                    "nBins": 6
                },
                {
                    "func": "n_excluded_bjets",
                    "xMin": 0,
                    "xMax": 4,
                    "nBins": 4
                },
                {
                    "func": "n_excluded_ljets",
                    "xMin": 0,
                    "xMax": 4,
                    "nBins": 4
                },
                {
                    "func": "nBoostedTop_Mass120_180",
                    "xMin": 0,
                    "xMax": 2,
                    "nBins": 2
                },
                {
                    "func": "nBoostedTop_Mass120_180_fRec02",
                    "xMin": 0,
                    "xMax": 2,
                    "nBins": 2
                },
                {
                    "func": "nBoostedTopWP1",
                    "xMin": 0,
                    "xMax": 2,
                    "nBins": 2
                },
                {
                    "func": "nBoostedTopWP2",
                    "xMin": 0,
                    "xMax": 2,
                    "nBins": 2
                },
            ]
        }
        of = open("job_{0}.json".format(ijob), "w")
        of.write(json.dumps(ret, indent=2))
        of.close()
        ijob += 1
